# -*- coding: utf-8 -*- #
# Copyright 2016 Google LLC. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Creates a new Cloud SQL instance."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from apitools.base.py import exceptions as apitools_exceptions

from googlecloudsdk.api_lib.sql import api_util as common_api_util
from googlecloudsdk.api_lib.sql import exceptions as sql_exceptions
from googlecloudsdk.api_lib.sql import operations
from googlecloudsdk.api_lib.sql import validate
from googlecloudsdk.calliope import base
from googlecloudsdk.calliope import exceptions
from googlecloudsdk.command_lib.kms import resource_args as kms_resource_args
from googlecloudsdk.command_lib.sql import flags
from googlecloudsdk.command_lib.sql import instances as command_util
from googlecloudsdk.command_lib.sql import validate as command_validate
from googlecloudsdk.command_lib.util.args import labels_util
from googlecloudsdk.core import log
from googlecloudsdk.core import properties
from googlecloudsdk.core.resource import resource_lex
from googlecloudsdk.core.resource import resource_property
import six

# 1h, based off of the max time it usually takes to create a SQL instance.
_INSTANCE_CREATION_TIMEOUT_SECONDS = 3600

DETAILED_HELP = {
    'EXAMPLES':
        """\
        To create a MySQL 5.7 instance with ID ``prod-instance'' that has 2
        CPUs, 4 GB of RAM, and is in the region ``us-central1'' (a zone will be
        auto-assigned), where the 'root' user has its password set to
        ``password123'', run:

          $ {command} prod-instance --database-version=MYSQL_5_7 --cpu=2 --memory=4GB --region=us-central1 --root-password=password123

        To create a Postgres 9.6 instance with ID ``prod-instance'' that has 2
        CPUs, 8 GiB of RAM, and is in the zone ``us-central1-a'', where the
        'postgres' user has its password set to ``password123'', run:

          $ {command} prod-instance --database-version=POSTGRES_9_6 --cpu=2 --memory=8GiB --zone=us-central1-a --root-password=password123

        To create a SQL Server 2017 Express instance with ID ``prod-instance''
        that has 2 CPUs, 3840MiB of RAM, and is in the zone ``us-central1-a'',
        where the 'sqlserver' user has its password set to ``password123'',
        run:

          $ {command} prod-instance --database-version=SQLSERVER_2017_EXPRESS --cpu=2 --memory=3840MiB --zone=us-central1-a --root-password=password123
        """,
}


def AddBaseArgs(parser, is_alpha=False):
  """Declare flag and positional arguments for this command parser."""
  # TODO(b/35705305): move common flags to command_lib.sql.flags
  base.ASYNC_FLAG.AddToParser(parser)
  parser.display_info.AddFormat(flags.GetInstanceListFormat())
  flags.AddActivationPolicy(parser)
  flags.AddActiveDirectoryDomain(parser)
  flags.AddAssignIp(parser)
  flags.AddAuthorizedNetworks(parser)
  flags.AddAvailabilityType(parser)
  parser.add_argument(
      '--backup',
      required=False,
      action='store_true',
      default=True,
      help='Enables daily backup.')
  flags.AddBackupStartTime(parser)
  flags.AddBackupLocation(parser, allow_empty=False)
  flags.AddCPU(parser)
  flags.AddInstanceCollation(parser)
  flags.AddDatabaseFlags(parser)
  flags.AddEnableBinLog(parser, show_negated_in_help=False)
  flags.AddRetainedBackupsCount(parser)
  flags.AddRetainedTransactionLogDays(parser)

  parser.add_argument(
      '--failover-replica-name',
      required=False,
      help='Also create a failover replica with the specified name.')
  parser.add_argument(
      'instance',
      type=command_validate.InstanceNameRegexpValidator(),
      help='Cloud SQL instance ID.')
  flags.AddMaintenanceReleaseChannel(parser)
  flags.AddMaintenanceWindowDay(parser)
  flags.AddMaintenanceWindowHour(parser)
  flags.AddDenyMaintenancePeriodStartDate(parser)
  flags.AddDenyMaintenancePeriodEndDate(parser)
  flags.AddDenyMaintenancePeriodTime(parser)
  flags.AddInsightsConfigQueryInsightsEnabled(parser, show_negated_in_help=True)
  flags.AddInsightsConfigQueryStringLength(parser)
  flags.AddInsightsConfigRecordApplicationTags(
      parser, show_negated_in_help=True)
  flags.AddInsightsConfigRecordClientAddress(parser, show_negated_in_help=True)
  flags.AddInsightsConfigQueryPlansPerMinute(parser)
  parser.add_argument(
      '--master-instance-name',
      required=False,
      help=('Name of the instance which will act as master in the '
            'replication setup. The newly created instance will be a read '
            'replica of the specified master instance.'))
  flags.AddMemory(parser)
  flags.AddPasswordPolicyMinLength(parser)
  flags.AddPasswordPolicyComplexity(parser)
  flags.AddPasswordPolicyReuseInterval(parser)
  flags.AddPasswordPolicyDisallowUsernameSubstring(parser)
  flags.AddPasswordPolicyPasswordChangeInterval(parser)
  flags.AddPasswordPolicyEnablePasswordPolicy(parser)
  parser.add_argument(
      '--replica-type',
      choices=['READ', 'FAILOVER'],
      help='The type of replica to create.')
  flags.AddReplication(parser)
  parser.add_argument(
      '--require-ssl',
      required=False,
      action='store_true',
      default=None,
      help='Specified if users connecting over IP must use SSL.')
  flags.AddRootPassword(parser)
  flags.AddStorageAutoIncrease(parser)
  flags.AddStorageSize(parser)
  parser.add_argument(
      '--storage-type',
      required=False,
      choices=['SSD', 'HDD'],
      default=None,
      help='The storage type for the instance. The default is SSD.')
  flags.AddTier(parser, is_alpha=is_alpha)
  kms_flag_overrides = {
      'kms-key': '--disk-encryption-key',
      'kms-keyring': '--disk-encryption-key-keyring',
      'kms-location': '--disk-encryption-key-location',
      'kms-project': '--disk-encryption-key-project'
  }
  kms_resource_args.AddKmsKeyResourceArg(
      parser,
      'instance',
      flag_overrides=kms_flag_overrides)
  flags.AddEnablePointInTimeRecovery(parser)
  flags.AddNetwork(parser)
  flags.AddSqlServerAudit(parser)
  flags.AddDeletionProtection(parser)
  flags.AddSqlServerTimeZone(parser)
  flags.AddConnectorEnforcement(parser)
  flags.AddTimeout(parser, _INSTANCE_CREATION_TIMEOUT_SECONDS)
  flags.AddEnableGooglePrivatePath(parser)


def AddBetaArgs(parser):
  """Declare beta flag and positional arguments for this command parser."""
  flags.AddExternalMasterGroup(parser)
  flags.AddInstanceResizeLimit(parser)
  flags.AddAllocatedIpRangeName(parser)
  labels_util.AddCreateLabelsFlags(parser)
  psc_setup_group = parser.add_group(hidden=True)
  flags.AddEnablePrivateServiceConnect(psc_setup_group)
  flags.AddAllowedPscProjects(psc_setup_group)


def AddAlphaArgs(unused_parser):
  """Declare alpha flags for this command parser."""
  pass


def RunBaseCreateCommand(args, release_track):
  """Creates a new Cloud SQL instance.

  Args:
    args: argparse.Namespace, The arguments that this command was invoked with.
    release_track: base.ReleaseTrack, the release track that this was run under.

  Returns:
    A dict object representing the operations resource describing the create
    operation if the create was successful.
  Raises:
    HttpException: A http error response was received while executing api
        request.
    ArgumentError: An argument supplied by the user was incorrect, such as
      specifying an invalid CMEK configuration or attempting to create a V1
      instance.
    RequiredArgumentException: A required argument was not supplied by the user,
      such as omitting --root-password on a SQL Server instance.
  """
  client = common_api_util.SqlClient(common_api_util.API_VERSION_DEFAULT)
  sql_client = client.sql_client
  sql_messages = client.sql_messages

  validate.ValidateInstanceName(args.instance)
  validate.ValidateInstanceLocation(args)
  instance_ref = client.resource_parser.Parse(
      args.instance,
      params={'project': properties.VALUES.core.project.GetOrFail},
      collection='sql.instances')

  # Get the region, tier, and database version from the master if these fields
  # are not specified.
  # TODO(b/64266672): Remove once API does not require these fields.
  if args.IsSpecified('master_instance_name'):
    master_instance_ref = client.resource_parser.Parse(
        args.master_instance_name,
        params={'project': properties.VALUES.core.project.GetOrFail},
        collection='sql.instances')
    try:
      master_instance_resource = sql_client.instances.Get(
          sql_messages.SqlInstancesGetRequest(
              project=instance_ref.project,
              instance=master_instance_ref.instance))
    except apitools_exceptions.HttpError as error:
      # TODO(b/64292220): Remove once API gives helpful error message.
      log.debug('operation : %s', six.text_type(master_instance_ref))
      exc = exceptions.HttpException(error)
      if resource_property.Get(exc.payload.content,
                               resource_lex.ParseKey('error.errors[0].reason'),
                               None) == 'notAuthorized':
        msg = ('You are either not authorized to access the master instance or '
               'it does not exist.')
        raise exceptions.HttpException(msg)
      raise
    if not args.IsSpecified('region'):
      args.region = master_instance_resource.region
    if not args.IsSpecified('database_version'):
      args.database_version = master_instance_resource.databaseVersion.name
    if not args.IsSpecified('tier') and not (
        args.IsSpecified('cpu') or
        args.IsSpecified('memory')) and master_instance_resource.settings:
      args.tier = master_instance_resource.settings.tier

    # Validate master/replica CMEK configurations.
    if master_instance_resource.diskEncryptionConfiguration:
      if args.region == master_instance_resource.region:
        # Warn user that same-region replicas inherit their master's CMEK
        # configuration.
        command_util.ShowCmekWarning('replica', 'the master instance')
      elif not args.IsSpecified('disk_encryption_key'):
        # Raise error that cross-region replicas require their own CMEK key if
        # the master is CMEK.
        raise exceptions.RequiredArgumentException(
            '--disk-encryption-key',
            '`--disk-encryption-key` is required when creating a cross-region '
            'replica of an instance with customer-managed encryption.')
      else:
        command_util.ShowCmekWarning('replica')
    elif args.IsSpecified('disk_encryption_key'):
      # Raise error that cross-region replicas cannot be CMEK encrypted if their
      # master is not.
      raise sql_exceptions.ArgumentError(
          '`--disk-encryption-key` cannot be specified when creating a replica '
          'of an instance without customer-managed encryption.')

  # --root-password is required when creating SQL Server instances
  if args.IsSpecified('database_version') and args.database_version.startswith(
      'SQLSERVER') and not args.IsSpecified('root_password'):
    raise exceptions.RequiredArgumentException(
        '--root-password',
        '`--root-password` is required when creating SQL Server instances.')

  if not args.backup:
    if args.IsSpecified('enable_bin_log'):
      raise sql_exceptions.ArgumentError(
          '`--enable-bin-log` cannot be specified when --no-backup is '
          'specified')
    elif args.IsSpecified('enable_point_in_time_recovery'):
      raise sql_exceptions.ArgumentError(
          '`--enable-point-in-time-recovery` cannot be specified when '
          '--no-backup is specified')

  if (args.IsKnownAndSpecified('allowed_psc_projects') and
      not args.IsKnownAndSpecified('enable_private_service_connect')):
    raise sql_exceptions.ArgumentError(
        '`--allowed-psc-projects` requires '
        '`--enable-private-service-connect`')

  if release_track == base.ReleaseTrack.ALPHA:
    if args.IsSpecified('workload_tier'):
      if not (args.IsSpecified('cpu') and args.IsSpecified('memory')):
        raise sql_exceptions.ArgumentError(
            '`--workload-tier` requires `--cpu` and `--memory`')

  instance_resource = (
      command_util.InstancesV1Beta4.ConstructCreateInstanceFromArgs(
          sql_messages,
          args,
          instance_ref=instance_ref,
          release_track=release_track))

  operation_ref = None
  try:
    result_operation = sql_client.instances.Insert(
        sql_messages.SqlInstancesInsertRequest(
            databaseInstance=instance_resource,
            project=instance_ref.project))

    operation_ref = client.resource_parser.Create(
        'sql.operations',
        operation=result_operation.name,
        project=instance_ref.project)

    if args.async_:
      if not args.IsSpecified('format'):
        args.format = 'default'
      return sql_client.operations.Get(
          sql_messages.SqlOperationsGetRequest(
              project=operation_ref.project, operation=operation_ref.operation))

    operations.OperationsV1Beta4.WaitForOperation(
        sql_client,
        operation_ref,
        'Creating Cloud SQL instance for ' + args.database_version,
        max_wait_seconds=args.timeout)

    log.CreatedResource(instance_ref)

    new_resource = sql_client.instances.Get(
        sql_messages.SqlInstancesGetRequest(
            project=instance_ref.project, instance=instance_ref.instance))
    return new_resource
  except apitools_exceptions.HttpError as error:
    log.debug('operation : %s', six.text_type(operation_ref))
    exc = exceptions.HttpException(error)
    if resource_property.Get(exc.payload.content,
                             resource_lex.ParseKey('error.errors[0].reason'),
                             None) == 'errorMaxInstancePerLabel':
      msg = resource_property.Get(exc.payload.content,
                                  resource_lex.ParseKey('error.message'), None)
      raise exceptions.HttpException(msg)
    raise


@base.ReleaseTracks(base.ReleaseTrack.GA)
class Create(base.Command):
  """Creates a new Cloud SQL instance."""

  detailed_help = DETAILED_HELP

  def Run(self, args):
    return RunBaseCreateCommand(args, self.ReleaseTrack())

  @staticmethod
  def Args(parser):
    """Args is called by calliope to gather arguments for this command."""
    AddBaseArgs(parser)
    flags.AddLocationGroup(parser)
    flags.AddDatabaseVersion(parser)


@base.ReleaseTracks(base.ReleaseTrack.BETA)
class CreateBeta(base.Command):
  """Creates a new Cloud SQL instance."""

  detailed_help = DETAILED_HELP

  def Run(self, args):
    return RunBaseCreateCommand(args, self.ReleaseTrack())

  @staticmethod
  def Args(parser):
    """Args is called by calliope to gather arguments for this command."""
    AddBaseArgs(parser)
    flags.AddLocationGroup(parser)
    AddBetaArgs(parser)
    flags.AddDatabaseVersion(parser, restrict_choices=False)


@base.ReleaseTracks(base.ReleaseTrack.ALPHA)
class CreateAlpha(base.Command):
  """Creates a new Cloud SQL instance."""

  detailed_help = DETAILED_HELP

  def Run(self, args):
    return RunBaseCreateCommand(args, self.ReleaseTrack())

  @staticmethod
  def Args(parser):
    """Args is called by calliope to gather arguments for this command."""
    AddBaseArgs(parser, is_alpha=True)
    flags.AddLocationGroup(parser)
    AddBetaArgs(parser)
    AddAlphaArgs(parser)
    flags.AddDatabaseVersion(parser, restrict_choices=False)

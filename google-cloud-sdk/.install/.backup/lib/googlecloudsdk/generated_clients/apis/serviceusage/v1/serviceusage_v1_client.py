"""Generated client library for serviceusage version v1."""
# NOTE: This file is autogenerated and should not be edited by hand.

from __future__ import absolute_import

from apitools.base.py import base_api
from googlecloudsdk.generated_clients.apis.serviceusage.v1 import serviceusage_v1_messages as messages


class ServiceusageV1(base_api.BaseApiClient):
  """Generated client library for service serviceusage version v1."""

  MESSAGES_MODULE = messages
  BASE_URL = 'https://serviceusage.googleapis.com/'
  MTLS_BASE_URL = 'https://serviceusage.mtls.googleapis.com/'

  _PACKAGE = 'serviceusage'
  _SCOPES = ['https://www.googleapis.com/auth/cloud-platform', 'https://www.googleapis.com/auth/cloud-platform.read-only', 'https://www.googleapis.com/auth/service.management']
  _VERSION = 'v1'
  _CLIENT_ID = 'CLIENT_ID'
  _CLIENT_SECRET = 'CLIENT_SECRET'
  _USER_AGENT = 'google-cloud-sdk'
  _CLIENT_CLASS_NAME = 'ServiceusageV1'
  _URL_VERSION = 'v1'
  _API_KEY = None

  def __init__(self, url='', credentials=None,
               get_credentials=True, http=None, model=None,
               log_request=False, log_response=False,
               credentials_args=None, default_global_params=None,
               additional_http_headers=None, response_encoding=None):
    """Create a new serviceusage handle."""
    url = url or self.BASE_URL
    super(ServiceusageV1, self).__init__(
        url, credentials=credentials,
        get_credentials=get_credentials, http=http, model=model,
        log_request=log_request, log_response=log_response,
        credentials_args=credentials_args,
        default_global_params=default_global_params,
        additional_http_headers=additional_http_headers,
        response_encoding=response_encoding)
    self.operations = self.OperationsService(self)
    self.services = self.ServicesService(self)

  class OperationsService(base_api.BaseApiService):
    """Service class for the operations resource."""

    _NAME = 'operations'

    def __init__(self, client):
      super(ServiceusageV1.OperationsService, self).__init__(client)
      self._upload_configs = {
          }

    def Cancel(self, request, global_params=None):
      r"""Starts asynchronous cancellation on a long-running operation. The server makes a best effort to cancel the operation, but success is not guaranteed. If the server doesn't support this method, it returns `google.rpc.Code.UNIMPLEMENTED`. Clients can use Operations.GetOperation or other methods to check whether the cancellation succeeded or whether the operation completed despite cancellation. On successful cancellation, the operation is not deleted; instead, it becomes an operation with an Operation.error value with a google.rpc.Status.code of 1, corresponding to `Code.CANCELLED`.

      Args:
        request: (ServiceusageOperationsCancelRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Empty) The response message.
      """
      config = self.GetMethodConfig('Cancel')
      return self._RunMethod(
          config, request, global_params=global_params)

    Cancel.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1/operations/{operationsId}:cancel',
        http_method='POST',
        method_id='serviceusage.operations.cancel',
        ordered_params=['name'],
        path_params=['name'],
        query_params=[],
        relative_path='v1/{+name}:cancel',
        request_field='cancelOperationRequest',
        request_type_name='ServiceusageOperationsCancelRequest',
        response_type_name='Empty',
        supports_download=False,
    )

    def Delete(self, request, global_params=None):
      r"""Deletes a long-running operation. This method indicates that the client is no longer interested in the operation result. It does not cancel the operation. If the server doesn't support this method, it returns `google.rpc.Code.UNIMPLEMENTED`.

      Args:
        request: (ServiceusageOperationsDeleteRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Empty) The response message.
      """
      config = self.GetMethodConfig('Delete')
      return self._RunMethod(
          config, request, global_params=global_params)

    Delete.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1/operations/{operationsId}',
        http_method='DELETE',
        method_id='serviceusage.operations.delete',
        ordered_params=['name'],
        path_params=['name'],
        query_params=[],
        relative_path='v1/{+name}',
        request_field='',
        request_type_name='ServiceusageOperationsDeleteRequest',
        response_type_name='Empty',
        supports_download=False,
    )

    def Get(self, request, global_params=None):
      r"""Gets the latest state of a long-running operation. Clients can use this method to poll the operation result at intervals as recommended by the API service.

      Args:
        request: (ServiceusageOperationsGetRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Operation) The response message.
      """
      config = self.GetMethodConfig('Get')
      return self._RunMethod(
          config, request, global_params=global_params)

    Get.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1/operations/{operationsId}',
        http_method='GET',
        method_id='serviceusage.operations.get',
        ordered_params=['name'],
        path_params=['name'],
        query_params=[],
        relative_path='v1/{+name}',
        request_field='',
        request_type_name='ServiceusageOperationsGetRequest',
        response_type_name='Operation',
        supports_download=False,
    )

    def List(self, request, global_params=None):
      r"""Lists operations that match the specified filter in the request. If the server doesn't support this method, it returns `UNIMPLEMENTED`. NOTE: the `name` binding allows API services to override the binding to use different resource name schemes, such as `users/*/operations`. To override the binding, API services can add a binding such as `"/v1/{name=users/*}/operations"` to their service configuration. For backwards compatibility, the default name includes the operations collection id, however overriding users must ensure the name binding is the parent resource, without the operations collection id.

      Args:
        request: (ServiceusageOperationsListRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (ListOperationsResponse) The response message.
      """
      config = self.GetMethodConfig('List')
      return self._RunMethod(
          config, request, global_params=global_params)

    List.method_config = lambda: base_api.ApiMethodInfo(
        http_method='GET',
        method_id='serviceusage.operations.list',
        ordered_params=[],
        path_params=[],
        query_params=['filter', 'name', 'pageSize', 'pageToken'],
        relative_path='v1/operations',
        request_field='',
        request_type_name='ServiceusageOperationsListRequest',
        response_type_name='ListOperationsResponse',
        supports_download=False,
    )

  class ServicesService(base_api.BaseApiService):
    """Service class for the services resource."""

    _NAME = 'services'

    def __init__(self, client):
      super(ServiceusageV1.ServicesService, self).__init__(client)
      self._upload_configs = {
          }

    def BatchEnable(self, request, global_params=None):
      r"""Enable multiple services on a project. The operation is atomic: if enabling any service fails, then the entire batch fails, and no state changes occur. To enable a single service, use the `EnableService` method instead.

      Args:
        request: (ServiceusageServicesBatchEnableRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Operation) The response message.
      """
      config = self.GetMethodConfig('BatchEnable')
      return self._RunMethod(
          config, request, global_params=global_params)

    BatchEnable.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1/{v1Id}/{v1Id1}/services:batchEnable',
        http_method='POST',
        method_id='serviceusage.services.batchEnable',
        ordered_params=['parent'],
        path_params=['parent'],
        query_params=[],
        relative_path='v1/{+parent}/services:batchEnable',
        request_field='batchEnableServicesRequest',
        request_type_name='ServiceusageServicesBatchEnableRequest',
        response_type_name='Operation',
        supports_download=False,
    )

    def BatchGet(self, request, global_params=None):
      r"""Returns the service configurations and enabled states for a given list of services.

      Args:
        request: (ServiceusageServicesBatchGetRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (BatchGetServicesResponse) The response message.
      """
      config = self.GetMethodConfig('BatchGet')
      return self._RunMethod(
          config, request, global_params=global_params)

    BatchGet.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1/{v1Id}/{v1Id1}/services:batchGet',
        http_method='GET',
        method_id='serviceusage.services.batchGet',
        ordered_params=['parent'],
        path_params=['parent'],
        query_params=['names'],
        relative_path='v1/{+parent}/services:batchGet',
        request_field='',
        request_type_name='ServiceusageServicesBatchGetRequest',
        response_type_name='BatchGetServicesResponse',
        supports_download=False,
    )

    def Disable(self, request, global_params=None):
      r"""Disable a service so that it can no longer be used with a project. This prevents unintended usage that may cause unexpected billing charges or security leaks. It is not valid to call the disable method on a service that is not currently enabled. Callers will receive a `FAILED_PRECONDITION` status if the target service is not currently enabled.

      Args:
        request: (ServiceusageServicesDisableRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Operation) The response message.
      """
      config = self.GetMethodConfig('Disable')
      return self._RunMethod(
          config, request, global_params=global_params)

    Disable.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1/{v1Id}/{v1Id1}/services/{servicesId}:disable',
        http_method='POST',
        method_id='serviceusage.services.disable',
        ordered_params=['name'],
        path_params=['name'],
        query_params=[],
        relative_path='v1/{+name}:disable',
        request_field='disableServiceRequest',
        request_type_name='ServiceusageServicesDisableRequest',
        response_type_name='Operation',
        supports_download=False,
    )

    def Enable(self, request, global_params=None):
      r"""Enable a service so that it can be used with a project.

      Args:
        request: (ServiceusageServicesEnableRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Operation) The response message.
      """
      config = self.GetMethodConfig('Enable')
      return self._RunMethod(
          config, request, global_params=global_params)

    Enable.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1/{v1Id}/{v1Id1}/services/{servicesId}:enable',
        http_method='POST',
        method_id='serviceusage.services.enable',
        ordered_params=['name'],
        path_params=['name'],
        query_params=[],
        relative_path='v1/{+name}:enable',
        request_field='enableServiceRequest',
        request_type_name='ServiceusageServicesEnableRequest',
        response_type_name='Operation',
        supports_download=False,
    )

    def Get(self, request, global_params=None):
      r"""Returns the service configuration and enabled state for a given service.

      Args:
        request: (ServiceusageServicesGetRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (GoogleApiServiceusageV1Service) The response message.
      """
      config = self.GetMethodConfig('Get')
      return self._RunMethod(
          config, request, global_params=global_params)

    Get.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1/{v1Id}/{v1Id1}/services/{servicesId}',
        http_method='GET',
        method_id='serviceusage.services.get',
        ordered_params=['name'],
        path_params=['name'],
        query_params=[],
        relative_path='v1/{+name}',
        request_field='',
        request_type_name='ServiceusageServicesGetRequest',
        response_type_name='GoogleApiServiceusageV1Service',
        supports_download=False,
    )

    def List(self, request, global_params=None):
      r"""List all services available to the specified project, and the current state of those services with respect to the project. The list includes all public services, all services for which the calling user has the `servicemanagement.services.bind` permission, and all services that have already been enabled on the project. The list can be filtered to only include services in a specific state, for example to only include services enabled on the project. WARNING: If you need to query enabled services frequently or across an organization, you should use [Cloud Asset Inventory API](https://cloud.google.com/asset-inventory/docs/apis), which provides higher throughput and richer filtering capability.

      Args:
        request: (ServiceusageServicesListRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (ListServicesResponse) The response message.
      """
      config = self.GetMethodConfig('List')
      return self._RunMethod(
          config, request, global_params=global_params)

    List.method_config = lambda: base_api.ApiMethodInfo(
        flat_path='v1/{v1Id}/{v1Id1}/services',
        http_method='GET',
        method_id='serviceusage.services.list',
        ordered_params=['parent'],
        path_params=['parent'],
        query_params=['filter', 'pageSize', 'pageToken'],
        relative_path='v1/{+parent}/services',
        request_field='',
        request_type_name='ServiceusageServicesListRequest',
        response_type_name='ListServicesResponse',
        supports_download=False,
    )

import requests
import json
import xxx_api_config

class V1APIClient:
    def __init__(self, proxies=None):
        self.base_url = xxx_api_config.BASE_URL        
        self.user = xxx_api_config.USER
        self.pwd = xxx_api_config.PWD
        # self.api_token = xxx_api_config.API_TOKEN
        self.proxies = proxies

    def _make_request(self, method='GET', endpoint_url_path='/', query_params=None, json_body=None, data=None, files=None, headers_additional=None):
        url = self.base_url + endpoint_url_path
        headers_token = {'Authorization': f'Bearer {self.api_token}'}
        headers = headers_token.copy()
        headers.update(headers_additional or {})
        proxies = self.proxies

        try:
            response = requests.request(method, url, params=query_params, json=json_body, data=data, files=files, headers=headers, proxies=proxies)
            print(response.status_code)
            for k, v in response.headers.items():
                print(f'{k}: {v}')
            print('')
            
            # 检查 HTTP 状态码，如果不是 2xx，则引发异常
            response.raise_for_status()
            
            if 'application/json' in response.headers.get('Content-Type', '') and len(response.content):
                result_response = json.dumps(response.json(), indent=4)
            else:
                result_response = response.text

        except requests.exceptions.HTTPError as err_http:
            # 处理 HTTP 错误
            print(f"HTTP error occurred: {err_http}")
            # 或者抛出适当的异常
            return "(或者抛出适当的异常...)"
        
        return result_response



    def get_endpoint_data(self, endpointName=None):
        url_path = '/v3.0/eiqs/endpoints'        
        query_params = {'top': 50}    # Maybe use for no endpointName
        headers = {'TMV1-Query': f"(endpointName eq '{endpointName}')"}    # Query string have to use Single quotes.

        return self._make_request(method='GET', endpoint_url_path=url_path, query_params=query_params, headers_additional=headers)
    
    def get_table_sys_id(self, number):
        endpoint_url_path = '/table/sn_si_incident'
        headers = {"Content-Type":"application/json","Accept":"application/json"}
        query_params = {
            'sysparm_query': f'number={number}',
            'sysparm_fields': 'sys_id'
        }

        response = self._make_request(method='GET', endpoint_url_path=endpoint_url_path, headers=headers, query_params=query_params)

        return str(json.loads(response)['result'][0]['sys_id'])


def api_method(v1api_client, args, api_method_to_call):
    #### API to run ####    
    api_method_to_run = getattr(v1api_client, api_method_to_call, None)

    if api_method_to_run is None:
        result = "no this api method"
        return result

    if api_method_to_call == "get_endpoint_data":
        result = api_method_to_run(endpointName=args.get("endpointName"))
    elif api_method_to_call == "get_endpoint_activity_data":
        result = api_method_to_run(endpointHostName=args.get("endpointHostName"))

    elif api_method_to_call == "list_custom_scripts":
        result = api_method_to_run()

    elif api_method_to_call == "add_custom_script":
        result = api_method_to_run()

    elif api_method_to_call == "get_response_tasks":
        result = api_method_to_run()

    elif api_method_to_call == "download_response_task_results":
        result = api_method_to_run(task_id=args.get("task_id"))
    
    return result



def main():    
    proxies = { "http": "http://10.10.10.10:8080", "https": "http://10.10.10.10:8080" }
    v1api_client = V1APIClient(proxies=proxies)
    
    #### query_params ####
    args = {
        "endpointName": "PC-123",
        "endpointHostName": "PC-123",
        "task_id": "RM-20231219-00001"
    }
    ####################
    
    #### API to call ####
    api_method_to_call = "get_endpoint_data"
    # api_method_to_call = "get_endpoint_activity_data"
    # api_method_to_call = "list_custom_scripts"
    # api_method_to_call = "get_response_tasks"
    # api_method_to_call = "download_response_task_results"
    
    #### API to run ####
    result = api_method(v1api_client, args, api_method_to_call)
    print(result)
    



if __name__ == '__main__':
    main()

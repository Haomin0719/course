from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
import datetime
from lib.db_operation import DatabaseManager

from pandas import Timestamp
import re

class ViewSetValidate(object):
    
    """
    This method only check parameters count, and check parameter name
    For example:
    valid_params = [symbol, start_date, end_date]
    check:
    count = 3
    loop over [symbol, start_date, end_date] make sure the name is correct.
    """
    
    def check_params(self, payload, required_params, valid_params):
        # request body is empty
        if not payload:
            self.response = Response(data={"msg":"params is empty"})
            self.response.status_code = 402
            return False
        
        # request body contain invalid parameters
        invalid = set(payload.keys()) - set(valid_params)
        missing = set(required_params) - set(payload.keys())
        msg = ""
        
        # all parameters is valid
        if not invalid and not missing:
            for key in set(valid_params) - set(payload.keys()):
                payload[key] = None
            return True
        
        msg = msg + f"invalid parameters {invalid}" if invalid else msg
        msg = msg + f"required parameters {missing} is missing" if missing else msg
        self.response = Response(data={"msg":msg})        
        self.response.status_code = 402
        return False


class TestViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = None
    parser_classes = (JSONParser,)
    response = None
    required_params = []
    valid_params = []

    def create(self, request):
        response = Response(data={"msg": "Succeed"})
        response.status_code = 200
        return response


class QuotesSet(viewsets.ModelViewSet, ViewSetValidate):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (JSONParser,)
    response = None
    dbm = DatabaseManager()
    required_params = ["dataname"]
    valid_params = ["dataname"]

    def _validate(self, payload):
        return  self.check_params(payload, self.required_params, self.valid_params)
    
    # POST
    def create(self, request):

        if not self._validate(request.data):
            return self.response
        
        res = self.dbm.get_quotes(request.data)
        data = res
        
        # Not found entry in database
        if res == []:
            response = Response(data={"msg":"not found"})
            response.status_code = 404
            return response
        
        elif isinstance(res, dict):
            response = Response(data=res)
            response.status_code = 400
            return response
        
        response = Response(data={"msg":"Succeed",
                                  'detail': {
                                        'data':data
                                  }})
        
        response.status_code = 200
        return response
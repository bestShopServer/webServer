
import json
import decimal

code = {
    'success': '10000',
    'error': '10001'
}
res = {
    'msg': '',
    'data': '',
    'code': code['success'],
}

class DecimalEncoder(json.JSONEncoder):
    def _iterencode(self, o, markers=None):
        if isinstance(o, decimal.Decimal):
            # wanted a simple yield str(o) in the next line,
            # but that would mean a yield on the line with super(...),
            # which wouldn't work (see my comment below), so...
            return (str(o) for o in [o])
        return super(DecimalEncoder, self)._iterencode(o, markers)

def HttpResponse(self=None,success=True,data=None,rescode=code['success'],msg='',headers=None,count=None):
    # if self.status_code != 200:
    #     success = False

    if rescode != code['success']:
        res['code'] = rescode
        res['msg'] = msg if msg else '请求出错,请稍后再试！'
    else:
        if success:
            res['code'] = code['success']
            res['msg'] = msg if msg else '操作成功'
        else:
            res['code'] = code['error']
            res['msg'] = msg if msg else '请求出错,请稍后再试！'
    res['data'] = data
    res['count'] = count
    return json.dumps(res,cls=DecimalEncoder)
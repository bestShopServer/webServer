


import requests

token="""
TPvDQqPsQIxIg8g5tLv1Lmh88LhJkdfvGRmEHtz0aHcqaMWhVgE1Iu4fEDtUyiJ+dVapUbX7dVhD7gsahoxUE80IIUJ+z3DjTrr4z79FmuLm4fPehDDMmhxjQWAC1mCMCk8eRVLoKRLXIkqt4jXyjtcIiaHQsILWMwsZBksA3vAO98xm6WCfkXNrcIWrQ7l6LFh0F3X7Jaj5floHiYamvVxitBuOv1e7C3quUnz5LIw=
"""

res = requests.request(method='POST',url="http://localhost:8888/api/v1/sso/logout",data={
    "data":"iocMV3nOJRSFGIp9VxosA3GONaeqKXYJiygDOQJVPVSSXGUr+3Ws4UA0sia3tFkaAZn/hFm7Z2L4ZRAIeHuVqRjQBOBYlGdwYMobyMmTj+Y="
},headers={
    "Authorization":"51A/jiLjLzb7QR+nigwNjHWKThj8pZeM/Fobmp5/49FxTEhTVCu0juVFhKvzim8odQefFopTrsihdX4652karmk0m+eaczqIr33QfrYaLaePOFXyS1twzfKyneMEpd8IJTI4d3tY8BJrPqCSsYi2qtkqlLLJZPpKEaKhoXG4kecQY6vUiSAaF/v42H4u2L9UahTsaoLDgQDq0FNRn+I9Zdh0v8VFjex4OmOg6k+KIiw="
})

print(res.text)
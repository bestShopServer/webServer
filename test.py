




class A(object):
    def __init__(self,**kwargs):
        print(kwargs)



class B(A):

    def __init__(self,**kwargs):


        super(B, self).__init__(**kwargs)


B(name="张飞")
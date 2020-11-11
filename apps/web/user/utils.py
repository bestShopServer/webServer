
from peewee import JOIN
from models.user import User,UserLinkRole,\
        UserLinkBranch,UserRole,Branch,UserAuth,\
            UserLinkMerchant

from apps.web.user.serializers import UserSerializer

async def user_query(**kwargs):

    self = kwargs.get("self")
    query = kwargs.get("query",None)
    isUserRole = kwargs.get("isUserRole",False)
    isBranch = kwargs.get("isBranch",False)
    isMobile = kwargs.get("isMobile",False)
    isEmail = kwargs.get("isEmail",False)
    isLoginName = kwargs.get("isLoginName",False)

    name = self.data.get("name", None)
    role_id = self.data.get("role_id",None)
    branch_id = self.data.get("branch_id",None)
    mobile = self.data.get("mobile",None)
    status = self.data.get("status",None)

    if status and status != 'all':
        query = query.where(User.status == status)

    if name:
        query = query.where(User.name == name)

    query = query.where(User.userid << \
               [ item.userid \
                    for item in  \
                        await self.db.execute(UserLinkMerchant.select().where(UserLinkMerchant.merchant_id == self.user.merchant_id)) ])

    if role_id:

        query = query.where(User.userid << \
                   [ item.userid \
                        for item in  \
                            await self.db.execute(UserLinkRole.select().where(UserLinkRole.role_id == role_id)) ])

    if branch_id:
        query = query.where(User.userid << \
                   [ item.userid \
                        for item in  \
                            await self.db.execute(UserLinkBranch.select().where(UserLinkBranch.branch_id == branch_id)) ])

    if mobile:
        query = query.where(User.userid << \
                   [ item.userid \
                        for item in  \
                            await self.db.execute(UserAuth.select().where(UserAuth.account == mobile,UserAuth.type == '1')) ])

    query = query.order_by(User.updtime.desc()).paginate(self.data['page'], self.data['size'])

    obj = await self.db.execute(query)

    count = len(obj)

    userids = [item.userid for item in obj]

    if len(userids):

        if isLoginName:

            login_name_obj_tmp = await self.db.execute(
                UserAuth.select().\
                    where(UserAuth.userid << userids).\
                    where(UserAuth.type == '0')
            )

            for item in obj:
                item.login_name = None
                for item1 in login_name_obj_tmp:
                    if item.userid == item1.userid:
                        item.login_name = item1
                        break

        if isMobile:

            phone_obj_tmp = await self.db.execute(
                UserAuth.select().\
                    where(UserAuth.userid << userids).\
                    where(UserAuth.type == '1')
            )

            for item in obj:
                item.mobile = None
                for item1 in phone_obj_tmp:
                    if item.userid == item1.userid:
                        item.mobile = item1
                        break

        if isEmail:
            email_obj_tmp = await self.db.execute(
                UserAuth.select().\
                    where(UserAuth.userid << userids).\
                    where(UserAuth.type == '2')
            )

            for item in obj:
                item.email = None
                for item1 in email_obj_tmp:
                    if item.userid == item1.userid:
                        item.email = item1
                        break

        if isUserRole:
            user_role_obj_tmp = await self.db.execute(
                UserLinkRole.select(UserLinkRole,UserRole). \
                    join(UserRole, join_type=JOIN.INNER, on=(UserRole.role_id == UserLinkRole.role_id)). \
                    where(UserLinkRole.userid << userids)
            )

            for item in obj:
                for item1 in user_role_obj_tmp:
                    if item.userid == item1.userid:
                        if hasattr(item, "userlinkrole") and item.userlinkrole:
                            item.userlinkrole.append(item1)
                        else:
                            item.userlinkrole = [item1]
        if isBranch:

            user_branch_obj_tmp = await self.db.execute(
                UserLinkBranch.select(UserLinkBranch,Branch). \
                    join(Branch, join_type=JOIN.INNER, on=(Branch.branch_id == UserLinkBranch.branch_id)). \
                    where(UserLinkBranch.userid << userids)
            )

            for item in obj:
                for item1 in user_branch_obj_tmp:
                    if item.userid == item1.userid:
                        if hasattr(item, "userlinkbranch") and item.userlinkbranch:
                            item.userlinkbranch.append(item1)
                        else:
                            item.userlinkbranch = [item1]

        return {"data":UserSerializer(obj,many=True).data,"count":count}


from peewee import JOIN
from models.user import User,UserLinkRole,UserLinkBranch,UserRole,Branch,UserAuth

from apps.web.user.serializers import UserSerializer

async def user_query(**kwargs):

    self = kwargs.get("self")
    query = kwargs.get("query",None)
    isUserRole = kwargs.get("isUserRole",False)
    isBranch = kwargs.get("isBranch",False)
    isPhone = kwargs.get("isPhone",True)
    isEmail = kwargs.get("isEmail",True)

    name = self.data.get("name", None)
    role_id = self.data.get("role_id",None)

    if name:
        query = query.where(User.name == name)

    if role_id:

        query = query.where(User.userid << \
                   [ item.userid \
                        for item in  \
                            await self.db.execute(UserLinkRole.select().where(UserLinkRole.role_id == role_id)) ])

    query = query.order_by(User.updtime.desc()).paginate(self.data['page'], self.data['size'])

    obj = await self.db.execute(query)

    count = len(obj)

    userids = [item.userid for item in obj]

    if len(userids):

        if isPhone:

            phone_obj_tmp = await self.db.execute(
                UserAuth.select().\
                    where(UserAuth.userid << userids).\
                    where(UserAuth.type == '1')
            )

            for item in obj:
                item.phone = None
                for item1 in phone_obj_tmp:
                    if item.userid == item1.userid:
                        item.phone = item1
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
                UserLinkRole.select(). \
                    join(UserRole, join_type=JOIN.INNER, on=(UserRole.role_id == UserLinkRole.role_id)). \
                    where(UserLinkRole.userid << userids)
            )

            for item in obj:
                for item1 in user_role_obj_tmp:
                    if item.userid == item1.userid:
                        if hasattr(item, "user_role_link") and item.user_role_link:
                            item.user_role_link.append(item1)
                        else:
                            item.user_role_link = [item1]
        if isBranch:

            user_branch_obj_tmp = await self.db.execute(
                UserLinkBranch.select(). \
                    join(Branch, join_type=JOIN.INNER, on=(Branch.branch_id == UserLinkBranch.branch_id)). \
                    where(UserLinkBranch.userid << userids)
            )

            for item in obj:
                for item1 in user_branch_obj_tmp:
                    if item.userid == item1.userid:
                        if hasattr(item, "user_branch_link") and item.user_branch_link:
                            item.user_branch_link.append(item1)
                        else:
                            item.user_branch_link = [item1]

        return {"data":UserSerializer(obj,many=True).data,"count":count}

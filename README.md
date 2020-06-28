游客：
    可匿名查看任何人的朋友圈
登录用户：
    注册登录之后，才可 发表，评论，删除，修改

API:
    UserAPI 提供用户登录注册接口
    CommonAPI 提供公共接口 序列化(serializers),
                         权限认证(authentications),
                         响应(MyResponse),
                         异常(exceptions)
    PyqAPI 此为主业务逻辑 提供朋友圈操作接口(增删查改)
           匿名用户(未登录) 只能查看他人朋友圈
           注册登录之后才能 发表，评论，删除，更新 朋友圈

models:
    UserAPI:
        UserAPI.User 继承 AbstractUser 表 重写django原生 User 表
        UserAPI.TestUser 测试
    PyqAPI:
        PyqAPI.Pyq     朋友圈表,与用户表为一对多关系
        PyqAPI.Comment 评论表,与用户表一对多，与朋友圈表一对多

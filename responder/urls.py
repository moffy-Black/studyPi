from controllers import api, IndexController, LoginController

api.add_route('/', IndexController)
api.add_route('/login', LoginController)
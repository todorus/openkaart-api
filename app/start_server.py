from init import api
import regions.views
import authentication.views

api.run(host="0.0.0.0", debug=True)

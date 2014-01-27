#qpy:console
from twisted.web import server, resource
from twisted.internet import reactor
import json, datetime
class User:
 def __init__(self, name):
  self.name = name
  self.current_request = None
 def receiveMsg(self, request):
  self.current_request = request
  activeUsers[self.name] = datetime.datetime.now()
 def sendMsg(self, msg):
  print msg
  #print self.name + " receiving msg"
  if self.current_request:
   self.current_request.write(msg)
   self.current_request.finish()
   self.current_request = None
   #print "sent message to: " + self.name
class Room:
 roomusers = []
 deadusers = []
 def __init__(self, chame):
  self.chanName = chame
 def sendMsg(self, msg):
  
  for user in users:
   #print user + " sent a message: " + msg
    try:
     users[user].sendMsg(msg)
     
     
    except:
     pass
  
 def addUser(self, user):
  self.roomusers.append(user)
 def listUsers(self):
  return self.roomusers
def removeDeadUSERS():
 mcusers = users
 for user in mcusers:
  userelapsed = datetime.datetime.now() - activeUsers[user]
  if userelapsed > datetime.timedelta(minutes=5):
   del users[user]
   del activeUsers[user]
def messagePacket(name, msg):
 msgpkg = {}
 msgpkg['from'] = name
 msgpkg['msg'] = msg
 return json.dumps(msgpkg)
def createRoom(room):
 rooms[room] = Room(room)
users = {}
activeUsers = {}
rooms = {}
class Webirc(resource.Resource):
 isLeaf = True
 mainroom = Room("Main")
 def setHeaders(self, request):
  request.setHeader('Access-Control-Allow-Origin','*')
  request.setHeader('Access-Control-Allow-Methods','GET, POST')
  request.setHeader('Access-Control-Allow-Headers','x-prototype-version,x-requested-with')
  request.setHeader('Access-Control-Max-Age',2520)
  request.setHeader('Content-type','application/json')
 def render_GET(self, request):
  removeDeadUSERS()
  if (request.path == "/msgs"):
   self.setHeaders(request)
   user = request.args['id'][0]
   if user not in users.keys():
    users[user] = User(user)
    self.mainroom.addUser(user)
   users[user].receiveMsg(request)
   return server.NOT_DONE_YET
  if (request.path == "/lst"):
   self.setHeaders(request)
   pkg = {}
   pkg["users"] = self.mainroom.listUsers()
   
   return json.dumps(pkg)
  if (request.path == "/actv"):
   return str(activeUsers)
 def render_POST(self, request):
  if (request.path == "/msg"):
   self.setHeaders(request)
   data = request.args['data'][0]
   
   self.mainroom.sendMsg(data)
   
  if(request.path == "/crm"):
   roomname = request.args['room']
   createRoom(roomName)
  if(request.path == "/jrm"):
   roomname = request.args['room']
   userID = request.args['id']
   self.rooms[roomname].addUser(userID)
  return '200'
root = Webirc()
root.putChild('ajax', Webirc())
reactor.listenTCP(8080, server.Site(root))
reactor.run()

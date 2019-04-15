import endpoints

from google.appengine.ext import ndb
from protorpc import remote

from endpoints_proto_datastore.ndb import EndpointsModel

#MODEL
class Bicycle(EndpointsModel):
  _message_fields_schema = ('id', 'brand', 'kind','price', 'created')
  brand = ndb.StringProperty()
  kind = ndb.StringProperty()
  price = ndb.IntegerProperty()
  created = ndb.DateTimeProperty(auto_now_add=True)

######API######
@endpoints.api(name='bicycle', version='v1', description='API for a bicycle store')
class BicycleApi(remote.Service):

  #SAVE ITEM
  @Bicycle.method(path='bicycle', http_method='POST', name='bicycle.insert')
  def insert_bicycle(self, bicycle):
    bicycle.put()
    return bicycle
  
  #CONSULT ITEM INFORMATION
  @Bicycle.method(request_fields=('id',),
                  path='bicycles/{id}', http_method='GET', name='bicycle.get')
  def get_bicycle(self, bicycle):
    if not bicycle.from_datastore:
      raise endpoints.NotFoundException('Item not found.')
    return bicycle

  #DELETE ITEM
  @Bicycle.method(request_fields=('id',),
                  path='bicycles/{id}', http_method='DELETE', name='bicycle.delete')
  def delete_bicycle(self, bicycle):
    if not bicycle.from_datastore:
      raise endpoints.NotFoundException('Item not found.')
    bicycle.key.delete()
    return bicycle

  #UPDATE ITEM
  @Bicycle.method(request_message=Bicycle.ProtoModel(),
                  path='bicycles/{id}',http_method="PUT", name='bicycle.update')
  def update_bicycle(self, bicycle_proto_request):  
    def update_existing():
      existing = Bicycle.get_by_id(bicycle_proto_request.id)
      if existing is None:
        raise endpoints.NotFoundException('Not found error')

      bicycle_proto_request.id = None
      bicycle = Bicycle.FromMessage(bicycle_proto_request)
      bicycle.key = existing.key
      bicycle.put()
      return bicycle
    return ndb.transaction(update_existing)

  #LIST ITEMS  
  @Bicycle.query_method(path='bicycles', name='bicycle.list')
  def list_bicycles(self, query):
    return query

#START APPLICATION SERVER
application = endpoints.api_server([BicycleApi])

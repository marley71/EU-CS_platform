from drf_yasg.generators import OpenAPISchemaGenerator


class GetOnlySchemaGenerator(OpenAPISchemaGenerator):
    def should_include_endpoint(self, path, method, view, public):
        if method.lower() != 'get':
            return False
        return super().should_include_endpoint(path, method, view, public)

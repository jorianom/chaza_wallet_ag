from ldap3 import Server, Connection, ObjectDef, Reader, MODIFY_REPLACE, SIMPLE
from graphql import GraphQLError

# Conexión LDAP server
ldap_server = Server('ldap://10.59.247.8:389')
ldap_user = 'cn=admin,dc=chazawallet,dc=unal,dc=edu,dc=co'
ldap_password = 'admin'
base_dn = 'dc=chazawallet,dc=unal,dc=edu,dc=co'

conn = Connection(ldap_server, user=ldap_user, password=ldap_password)

# Crear
def ldap_create(conn, base_dn, username, password):
    conn.bind()
    if not conn.bind():
        raise GraphQLError('Error: fallo en LDAP bind para create')

    object_class = ['inetOrgPerson', 'organizationalPerson', 'person', 'top']
    attributes = {
        'cn': username,
        'sn': username,
        'mail': f"{username}@example.com",
        'userPassword': password
    }

    conn.add(f"cn={username}," + base_dn, object_class, attributes)

    conn.unbind()

# Leer
def ldap_read_all(conn, base_dn):
    conn.bind()
    if not conn.bind():
        raise GraphQLError('Error: fallo en LDAP bind para read_all')

    object_def = ObjectDef('inetOrgPerson', conn)
    reader = Reader(conn, object_def, base_dn)

    # Search for a specific entry by its CN (Common Name)
    search_result = reader.search(attributes=['cn', 'sn', 'mail', 'userPassword'])
    for entry in search_result:
        print(entry.entry_dn, entry)

    conn.unbind()

# Modificar
def ldap_update(conn, base_dn, username, password):
    conn.bind()
    if not conn.bind():
        raise GraphQLError('Error: fallo en LDAP bind para update')

    conn.modify(f"cn={username}," + base_dn, {'userPassword': [(MODIFY_REPLACE, [password])]})

    conn.unbind()

# Borrar
def ldap_delete(conn, base_dn, username):
    conn.bind()
    if not conn.bind():
        raise GraphQLError('Error: fallo en LDAP bind para delete')

    conn.delete(f"cn={username}," + base_dn)

    conn.unbind()

# Autenticar
def ldap_authenticate(base_dn, username, password):
    user_dn = f"cn={username},{base_dn}"

    try:
        conn = Connection(ldap_server, user=user_dn, password=password, authentication=SIMPLE)
        if not conn.bind():
            return False
        else:
            return True
    except Exception as e:
        print(f"Error de autenticación LDAP: {e}")
        return False

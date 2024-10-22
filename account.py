class NewAccount():
    def __init__(self,vault_id, name, email, password, url ,aes_iv,auth_tag, user_name=None,type=None):
        self.vault_id = vault_id
        self.name = name
        self.email = email
        self.password = password
        self.url = url
        self.user_name = user_name
        self.type = type
        self.aes_iv = aes_iv
        self.auth_tag = auth_tag


class Account():
    def __init__(self, id, vault_id, name, user_name, email, password, type, url, aes_iv, auth_tag, created_at, updated_at ):
        self.id = id
        self.vault_id = vault_id
        self.name = name
        self.email = email
        self.password = password
        self.url = url
        self.user_name = user_name
        self.type = type
        self.aes_iv = aes_iv
        self.auth_tag = auth_tag
        self.created_at = created_at
        self.updated_at = updated_at



import hashlib
import sys

def create_password_hash(password):
    """Gera um hash SHA-256 para a password."""
    return hashlib.sha256(password.encode()).hexdigest()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python scripts/create_user.py <password>")
        sys.exit(1)
    
    password = sys.argv[1]
    hashed_password = create_password_hash(password)
    print("Por favor, adicione este hash à sua folha 'Credenciais' no Google Sheets.")
    print(f"Password: {password}")
    print(f"Hash: {hashed_password}")

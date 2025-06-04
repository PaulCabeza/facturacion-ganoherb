# Guía de Despliegue en Fly.io

## Prerrequisitos

1. **Instalar Fly CLI:**
   ```bash
   # macOS
   brew install flyctl
   
   # Linux/WSL
   curl -L https://fly.io/install.sh | sh
   ```

2. **Crear cuenta y autenticarse:**
   ```bash
   flyctl auth signup
   # o si ya tienes cuenta
   flyctl auth login
   ```

## Configuración del Proyecto

### 1. Inicializar la aplicación en Fly.io
```bash
flyctl launch --no-deploy
```

**Nota:** Usa `--no-deploy` para configurar primero las variables de entorno.

### 2. Configurar variables de entorno
```bash
# Generar una SECRET_KEY segura
python -c "import secrets; print(secrets.token_urlsafe(50))"

# Configurar las variables
flyctl secrets set SECRET_KEY="tu-secret-key-generada"
flyctl secrets set DEBUG=False
flyctl secrets set ALLOWED_HOSTS="*.fly.dev,facturacion-ganoherb.site"
```

### 3. Configurar PostgreSQL (recomendado)
```bash
# Crear una base de datos PostgreSQL en Fly.io
flyctl postgres create --name facturacion-ganoherb-db --region mia

# Conectar la base de datos a tu aplicación
flyctl postgres attach --app facturacion-ganoherb facturacion-ganoherb-db
```

### 4. Crear directorio static (si no existe)
```bash
mkdir -p static
touch static/.gitkeep
```

## Despliegue

### 1. Desplegar la aplicación
```bash
flyctl deploy
```

### 2. Crear superusuario (opcional)
```bash
flyctl ssh console
python manage.py createsuperuser
exit
```

### 3. Verificar el despliegue
```bash
flyctl status
flyctl logs
```

## Variables de Entorno Necesarias

- `SECRET_KEY`: Clave secreta de Django
- `DEBUG`: False para producción
- `ALLOWED_HOSTS`: Dominios permitidos
- `DATABASE_URL`: Se configura automáticamente al conectar PostgreSQL

## Comandos Útiles

```bash
# Ver logs en tiempo real
flyctl logs --app facturacion-ganoherb

# Ver el estado de la aplicación
flyctl status --app facturacion-ganoherb

# Escalar la aplicación
flyctl scale count 2 --app facturacion-ganoherb

# SSH a la aplicación
flyctl ssh console --app facturacion-ganoherb

# Reiniciar la aplicación
flyctl restart --app facturacion-ganoherb
```

## Notas Importantes

1. **Dominio personalizado:** Si quieres usar tu dominio personalizado, ejecuta:
   ```bash
   flyctl certs create facturacion-ganoherb.site
   ```

2. **Volúmenes:** Si necesitas almacenamiento persistente para archivos media:
   ```bash
   flyctl volumes create media_data --size 1 --app facturacion-ganoherb
   ```

3. **Backup de base de datos:**
   ```bash
   flyctl postgres backup create --app facturacion-ganoherb-db
   ```

## Estructura de Archivos Creados

- `Dockerfile`: Configuración del contenedor
- `fly.toml`: Configuración de Fly.io
- `.dockerignore`: Archivos excluidos del build
- `requirements.txt`: Dependencias actualizadas
- `ganoherb_inventory_billing/settings.py`: Configuración de producción

## Troubleshooting

- Si hay problemas con archivos estáticos, verifica que `whitenoise` esté en requirements.txt
- Si hay errores de conexión a la base de datos, verifica las variables de entorno
- Para debugging, puedes cambiar temporalmente `DEBUG=True` con `flyctl secrets set DEBUG=True` 
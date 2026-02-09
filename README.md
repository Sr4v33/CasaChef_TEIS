# 🍳 CasaChef

**CasaChef** es una plataforma digital que conecta 👨‍🍳 *cocineros locales* con 👥 *clientes* que buscan **comida casera preparada bajo pedido**.

Funciona como un **marketplace transaccional** enfocado en la **gestión real del negocio del cocinero**, permitiendo controlar:

- 🗓️ Producción diaria  
- 🔢 Cupos disponibles  
- 🔄 Ciclo completo del pedido  

Todo esto evitando **sobreventas** y garantizando **trazabilidad** en cada orden.

A diferencia de las plataformas tradicionales de domicilios 🚴‍♂️, **CasaChef prioriza el dominio del negocio**:  
👉 producción  
👉 disponibilidad  
👉 estados del pedido  

---

## ✨ Características Principales

- 🍽️ Publicación de platos con **producción diaria limitada**
- 🔒 Control de cupos y **cierre automático de ventas**
- 📦 Gestión del **ciclo completo del pedido**
- 🧩 Separación clara entre **platos, producción y pedidos**
- 🚀 Arquitectura preparada para **escalar con nuevos módulos**

---

## 🛠️ Tecnologías

- 🐍 **Python 3**
- 🌐 **Django**
- 🗄️ **SQLite** (entorno de desarrollo)

---

## 🗂️ Estructura del Proyecto

```text
casachef/
│
├── apps/
│   ├── cooks        # Gestión de cocineros
│   ├── dishes       # Platos
│   ├── orders       # Pedidos
│   ├── production   # Producción diaria
│   └── users        # Usuarios
│
├── config/
├── manage.py
├── requirements.txt

```
## ⚙️ Instalación y Ejecución Local

### 1️⃣ Clonar el Repositorio
```
git clone https://github.com/Sr4v33/CasaChef---TEIS
cd casaChef
```

### 2️⃣ Crear Entorno Virtual
```
python -m venv venv
```
#### Activar el entorno: 
- 🪟 Windows:
```
venv\Scripts\activate
```
- 🐧 Linux/macOS
```
source venv/bin/activate
```

### 3️⃣ Instalar Dependencias
```
pip install -r requirements.txt
```

### 4️⃣ Configurar Variables de Entorno
Crear un achivo ```.env``` en la raíz:
```
DEBUG=True
SECRET_KEY=your-secret-key
```

### 5️⃣ Migraciones y Ejecución
Crear un achivo ```.env``` en la raíz:
```
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
#### 🔗 Accesos: 
- App Principal: ```http://127.0.0.1:8000/```
- Panel Admin: ```http://127.0.0.1:8000/admin```


## 🚧 Estado del Proyecto
Proyecto en fase inicial de construcción del **dominio** y **reglas de negocio**.

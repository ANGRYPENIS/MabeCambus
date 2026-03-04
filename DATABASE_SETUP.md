# CamBus Database Configuration Guide

## Overview

The `configure-db` scripts provide an interactive way to set up your PostgreSQL database for CamBus. They support two main workflows:

1. **Use Existing Database** - Connect to an already-configured database
2. **Create New Database** - Create a new PostgreSQL database with a new user, load the schema, and set up a demo account

Both scripts automatically create a `.env` file with the necessary database credentials.

---

## Features

✅ **Database Selection/Creation** - Choose existing or create new database  
✅ **User Management** - Create new PostgreSQL users with proper credentials  
✅ **Schema Initialization** - Automatically load `cambus.sql` to create tables  
✅ **Demo User Account** - Create a pre-configured demo account for testing  
✅ **Automatic .env Generation** - Create environment configuration file automatically  
✅ **Connection Validation** - Verify database connection before saving  
✅ **Backup Management** - Automatically backup previous .env files  

---

## Demo Account Details

When you complete database configuration, a demo user account is automatically created:

| Property | Value |
|----------|-------|
| **Username** | `demo` |
| **Password** | `demo_password` |
| **Role** | OPERADOR (Driver/Operator) |
| **Department** | DEMOSTRACION |

This account can be used to demonstrate the application without needing to create a new user in the admin panel.

---

## Platform-Specific Instructions

### Windows

**Requirements:**
- PostgreSQL installed ([Download](https://www.postgresql.org/download/windows/))
- `psql` command line tool available in PATH

**Running the script:**

```bash
configure-db.bat
```

The script will:
1. Display a menu with options
2. Ask for PostgreSQL credentials
3. List available databases or guide you through creating a new one
4. Create/update the `.env` file
5. Validate the configuration

---

### Linux / macOS

**Requirements:**
- PostgreSQL installed
- Bash shell

**Installation (if not already installed):**

```bash
# Ubuntu/Debian
sudo apt install postgresql postgresql-contrib

# macOS
brew install postgresql
```

**Running the script:**

```bash
./configure-db.sh
```

---

## Step-by-Step Workflows

### Option 1: Use Existing Database

Perfect if you already have PostgreSQL running with a database configured.

1. Run `configure-db.bat` (Windows) or `./configure-db.sh` (Linux/Mac)
2. Select **Option 1**
3. Enter PostgreSQL connection details:
   - **Host**: Where PostgreSQL is running (usually `localhost`)
   - **Port**: PostgreSQL port (default: `5432`)
   - **Username**: PostgreSQL user with database access
   - **Password**: User password
4. Select the database to use from the list
5. The script will:
   - Verify connection to the database
   - Create/update the demo user account
   - Generate `.env` file

---

### Option 2: Create New Database

Recommended for fresh installations or development environments.

1. Run `configure-db.bat` (Windows) or `./configure-db.sh` (Linux/Mac)
2. Select **Option 2**
3. Enter PostgreSQL admin credentials:
   - **Admin Host**: PostgreSQL server location (usually `localhost`)
   - **Admin Port**: PostgreSQL port (default: `5432`)
   - **Admin Username**: PostgreSQL superuser (usually `postgres`)
   - **Admin Password**: Superuser password
4. The script will verify admin connection
5. Enter new database details:
   - **Database Name**: Name for the new database (e.g., `cambus_db`)
   - **New Username**: PostgreSQL user for this database (e.g., `cambus_user`)
   - **New Password**: Password for the new user
6. The script will automatically:
   - Create the PostgreSQL user
   - Create the database
   - Load the entire `cambus.sql` schema
   - Create the demo user account
   - Generate `.env` file
   - Validate the complete setup

---

## What Gets Created

### Database Objects

The `cambus.sql` script creates:

- **Tables**: 
  - `usuarios` - Application user accounts
  - `andenes` - Loading dock information
  - `camaras` - Camera configurations
  - `registros_vehiculos` - Vehicle entry/exit records (partitioned by date)
  - `estancias_vehiculos` - Vehicle parking sessions
  - `turnos` - Work shifts
  - And more...

- **Extensions**: 
  - `uuid-ossp` - UUID generation
  - `pg_trgm` - Full-text search capabilities

- **Triggers & Indexes**: Auto-generated for performance

### Application User

The demo user created in the `usuarios` table:
- Username: `demo`
- Password hashed with bcrypt (algorithm: `$2b$12$...`)
- Role: `OPERADOR` (read-only access to dashboard and registration)
- Automatically active upon creation

---

## `.env` File Format

After configuration, your `.env` file will contain:

```bash
# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=cambus_db
DB_USER=cambus_user
DB_PASSWORD=your_password_here

# Application Settings
STREAMLIT_LOGGER_LEVEL=info
STREAMLIT_CLIENT_SHOW_ERROR_DETAILS=false
STREAMLIT_CLIENT_TOOLBAR_MODE=minimal
```

**Important:** Never commit `.env` to Git (it's in `.gitignore`)

---

## Troubleshooting

### "PostgreSQL not found"
- **Windows**: Install PostgreSQL from https://www.postgresql.org/download/windows/
- **Linux**: `sudo apt install postgresql postgresql-contrib`
- **macOS**: `brew install postgresql`

### "Cannot connect to PostgreSQL"
Verify:
- PostgreSQL service is running
- Correct host and port
- PostgreSQL user exists and password is correct
- Firewall allows connections to port 5432

### "Database does not exist" (Option 1)
Create the database first using Option 2 or PostgreSQL tools:
```sql
CREATE DATABASE cambus_db OWNER postgres;
```

### "Permission denied" (Option 2)
The PostgreSQL superuser password must be correct. On fresh installations, try:
- Windows: Run Command Prompt as Administrator
- Linux/Mac: May need `sudo` to interact with PostgreSQL

### ".env file not created"
Verify you have write permissions in the current directory:
```bash
# Linux/Mac
ls -l .env

# Windows
dir .env
```

---

## Complete Setup Workflow

Once your database is configured:

```bash
# 1. Run database configuration (creates .env)
configure-db.bat          # Windows
./configure-db.sh         # Linux/Mac

# 2. Install Python dependencies
setup.bat                 # Windows
./setup.sh                # Linux/Mac

# 3. Start the application
run.bat                   # Windows
./run.sh                  # Linux/Mac

# 4. Open browser to:
#    http://localhost:8501
#
# 5. Log in with:
#    Username: demo
#    Password: demo_password
```

---

## Resetting/Reconfiguring

### To reconfigure the database:

1. Run `configure-db` again - it will:
   - Create a timestamped backup of your previous `.env` (e.g., `.env.backup.20240304_143052`)
   - Overwrite `.env` with new configuration
   - Verify the new connection

2. Previous configuration is preserved in `.env.backup.*` files

### To reset the demo user password:

Update the user's password hash in the database:

```sql
-- Using psql
\c cambus_db

-- Update password to 'demo_password' (pre-hashed with bcrypt)
UPDATE usuarios 
SET password_hash = '$2b$12$YY7GWLRVHMPXkc9iOvN/NeHEbKKW6SH1lWHPEqPjKsHwSHVqXFU3G'
WHERE username = 'demo';

-- Verify
SELECT username, password_hash FROM usuarios WHERE username = 'demo';
```

---

## Security Notes

- **Never commit `.env` to Git** - It contains database passwords
- **Backup your `.env` file** - Store securely if the database password is sensitive
- **Change demo password before production** - The demo account uses a common password for testing
- **Create admin user** - After setup, create an ADMIN user for regular operations instead of using demo

---

## Additional Resources

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [psql Command Reference](https://www.postgresql.org/docs/current/app-psql.html)
- [CamBus README](README.md)
- [Troubleshooting Guide](TROUBLESHOOTING_WINDOWS.md)


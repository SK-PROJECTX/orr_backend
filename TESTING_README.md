# ORR Backend Testing Guide

## Test Files Overview

All test files are now located in the Django backend folder (`orr/`) for better organization.

### Available Tests

1. **`test_models_import.py`** - Tests Django model imports and basic functionality
2. **`test_auth_flow.py`** - Tests authentication login/logout flow
3. **`test_api_fix.py`** - Tests API endpoints and responses
4. **`test_image_upload.py`** - Tests image upload functionality with authentication
5. **`test_cms_integration.py`** - Tests CMS integration and content management

## Running Tests

### Run All Tests
```bash
cd orr
python run_tests.py
```

### Run Individual Tests
```bash
cd orr
python test_models_import.py
python test_auth_flow.py
python test_api_fix.py
python test_image_upload.py
python test_cms_integration.py
```

### Run Django Unit Tests
```bash
cd orr
python manage.py test
```

## Prerequisites

1. **Django server must be running:**
   ```bash
   cd orr
   python manage.py runserver
   ```

2. **Test user must exist:**
   ```bash
   cd orr
   python manage.py create_test_user --username editor --password editor123
   ```

3. **Required packages:**
   - `requests` (for API testing)
   - `Pillow` (for image testing)

## Test Descriptions

### Model Import Test
- Verifies all CMS models can be imported
- Tests model instantiation
- Checks default values

### Authentication Flow Test
- Tests login endpoint
- Verifies token generation
- Tests authenticated vs unauthenticated requests

### API Fix Test
- Tests all major API endpoints
- Verifies response formats
- Checks error handling

### Image Upload Test
- Tests file upload functionality
- Verifies authentication requirements
- Tests business system section updates

### CMS Integration Test
- Tests comprehensive content endpoint
- Verifies all content sections
- Tests content update functionality

## Expected Results

✅ **All tests should pass** when:
- Django server is running
- Database is migrated
- Test user exists
- All dependencies are installed

❌ **Tests may fail** if:
- Server is not running
- Authentication is not set up
- Database is not migrated
- Missing dependencies

## Troubleshooting

### Common Issues

1. **Connection Refused**
   - Ensure Django server is running on port 8000

2. **Authentication Errors**
   - Run `python manage.py create_test_user`

3. **Import Errors**
   - Ensure you're in the `orr/` directory
   - Check Django settings are configured

4. **Database Errors**
   - Run `python manage.py migrate`

### Debug Mode

Add `--verbose` flag to see detailed output:
```bash
python test_auth_flow.py --verbose
```

## Integration with CI/CD

These tests can be integrated into CI/CD pipelines:

```yaml
# Example GitHub Actions
- name: Run Backend Tests
  run: |
    cd orr
    python manage.py migrate
    python manage.py create_test_user
    python run_tests.py
```
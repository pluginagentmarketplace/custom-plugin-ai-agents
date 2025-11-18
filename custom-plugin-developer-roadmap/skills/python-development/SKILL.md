---
name: python-development
description: Master modern Python development with type hints, async/await, FastAPI, Pydantic, pytest, and virtual environments. Use when building Python applications, APIs, and async systems.
---

# Python Development

Master modern Python development with type hints, asynchronous programming, FastAPI, data validation, testing, and best practices.

## Quick Start

### Modern Python with Type Hints
```python
from typing import List, Dict, Optional, Union, Tuple
from dataclasses import dataclass

# Basic types
def greet(name: str) -> str:
    return f"Hello, {name}!"

# Collections
def process_items(items: List[str]) -> Dict[str, int]:
    return {item: len(item) for item in items}

# Optional types
def find_user(user_id: int) -> Optional[Dict[str, str]]:
    if user_id > 0:
        return {"id": str(user_id), "name": "User"}
    return None

# Union types
def parse_value(value: Union[int, str]) -> int:
    if isinstance(value, int):
        return value
    return int(value)

# Complex types
def fetch_data(ids: List[int]) -> Tuple[List[str], int]:
    return ["data1", "data2"], len(ids)
```

### Type Hints with Generics
```python
from typing import TypeVar, Generic, Protocol

T = TypeVar('T')

class Container(Generic[T]):
    def __init__(self, value: T) -> None:
        self.value = value

    def get(self) -> T:
        return self.value

# Usage
int_container: Container[int] = Container(42)
str_container: Container[str] = Container("hello")

# Protocol for duck typing
class Drawable(Protocol):
    def draw(self) -> None: ...

def render(obj: Drawable) -> None:
    obj.draw()
```

## Async/Await Programming

### Basic Async Functions
```python
import asyncio
from typing import List

async def fetch_data(url: str) -> str:
    """Simulate async data fetching."""
    await asyncio.sleep(1)  # Simulate I/O delay
    return f"Data from {url}"

async def main() -> None:
    # Sequential execution
    result1 = await fetch_data("http://api1.com")
    result2 = await fetch_data("http://api2.com")
    print(result1, result2)

# Run async function
asyncio.run(main())
```

### Concurrent Tasks
```python
async def fetch_multiple_urls(urls: List[str]) -> List[str]:
    """Fetch multiple URLs concurrently."""
    tasks = [fetch_data(url) for url in urls]
    results = await asyncio.gather(*tasks)
    return results

async def main() -> None:
    urls = ["http://api1.com", "http://api2.com", "http://api3.com"]
    results = await fetch_multiple_urls(urls)
    print(results)

asyncio.run(main())
```

### Async Context Manager
```python
from contextlib import asynccontextmanager
from typing import AsyncIterator

class Database:
    async def connect(self) -> None:
        await asyncio.sleep(0.1)
        print("Connected")

    async def disconnect(self) -> None:
        await asyncio.sleep(0.1)
        print("Disconnected")

@asynccontextmanager
async def get_db() -> AsyncIterator[Database]:
    db = Database()
    await db.connect()
    try:
        yield db
    finally:
        await db.disconnect()

async def main() -> None:
    async with get_db() as db:
        print("Using database")

asyncio.run(main())
```

### Async Iterator
```python
from typing import AsyncIterator

async def async_range(n: int) -> AsyncIterator[int]:
    for i in range(n):
        await asyncio.sleep(0.1)
        yield i

async def main() -> None:
    async for num in async_range(5):
        print(num)

asyncio.run(main())
```

## FastAPI Framework

### Basic API
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="My API", version="1.0.0")

# Request model
class Item(BaseModel):
    id: int
    name: str
    price: float
    description: Optional[str] = None

# Response model
class ItemResponse(BaseModel):
    id: int
    name: str
    price: float

# Route
@app.get("/items/", response_model=List[ItemResponse])
async def list_items() -> List[ItemResponse]:
    """Get all items."""
    return [
        ItemResponse(id=1, name="Item1", price=10.0),
        ItemResponse(id=2, name="Item2", price=20.0)
    ]

@app.get("/items/{item_id}", response_model=ItemResponse)
async def get_item(item_id: int) -> ItemResponse:
    """Get a specific item."""
    return ItemResponse(id=item_id, name="Item", price=15.0)

@app.post("/items/", response_model=ItemResponse)
async def create_item(item: Item) -> ItemResponse:
    """Create a new item."""
    return ItemResponse(id=1, name=item.name, price=item.price)

@app.put("/items/{item_id}", response_model=ItemResponse)
async def update_item(item_id: int, item: Item) -> ItemResponse:
    """Update an item."""
    return ItemResponse(id=item_id, name=item.name, price=item.price)

@app.delete("/items/{item_id}")
async def delete_item(item_id: int) -> dict:
    """Delete an item."""
    return {"message": f"Item {item_id} deleted"}
```

### Query and Path Parameters
```python
from fastapi import Query, Path

@app.get("/search/")
async def search(
    q: str = Query(..., min_length=3, max_length=50),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
) -> dict:
    """Search with query parameters."""
    return {"q": q, "skip": skip, "limit": limit}

@app.get("/items/{item_id}")
async def get_item_detailed(
    item_id: int = Path(..., gt=0, description="Item ID"),
    detailed: bool = Query(False)
) -> dict:
    """Get item with path and query parameters."""
    return {"item_id": item_id, "detailed": detailed}
```

### Request Body and Headers
```python
from fastapi import Header

class User(BaseModel):
    username: str
    email: str

@app.post("/users/")
async def create_user(
    user: User,
    x_token: str = Header(None)
) -> dict:
    """Create user with header validation."""
    return {"user": user, "token": x_token}
```

### Error Handling
```python
from fastapi import status

@app.get("/items/{item_id}")
async def get_item(item_id: int) -> ItemResponse:
    """Get item with error handling."""
    if item_id == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid item ID"
        )
    if item_id > 1000:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    return ItemResponse(id=item_id, name="Item", price=15.0)
```

### Dependency Injection
```python
from fastapi import Depends

async def get_query_token(token: str = Query(...)) -> str:
    """Validate token."""
    if token != "valid-token":
        raise HTTPException(status_code=401, detail="Invalid token")
    return token

@app.get("/protected/")
async def protected_route(token: str = Depends(get_query_token)) -> dict:
    """Protected route with token dependency."""
    return {"token": token, "message": "Access granted"}
```

### Background Tasks
```python
from fastapi import BackgroundTasks

def write_log(message: str) -> None:
    with open("log.txt", "a") as f:
        f.write(f"{message}\n")

@app.post("/send-notification/")
async def send_notification(
    email: str,
    background_tasks: BackgroundTasks
) -> dict:
    background_tasks.add_task(write_log, f"Notification sent to {email}")
    return {"message": "Notification queued"}
```

## Pydantic Data Validation

### Basic Models
```python
from pydantic import BaseModel, Field, validator, field_validator
from typing import Optional, List

class User(BaseModel):
    id: int
    name: str = Field(..., min_length=1, max_length=100)
    email: str
    age: Optional[int] = None
    tags: List[str] = []

# Parsing
user_data = {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "age": 30,
    "tags": ["python", "fastapi"]
}
user = User(**user_data)
print(user.dict())
print(user.json())
```

### Custom Validation
```python
from pydantic import field_validator, ValidationError

class Product(BaseModel):
    name: str
    price: float
    quantity: int

    @field_validator('price')
    @classmethod
    def price_must_be_positive(cls, v: float) -> float:
        if v < 0:
            raise ValueError('Price must be positive')
        return v

    @field_validator('name')
    @classmethod
    def name_must_not_be_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError('Name cannot be empty')
        return v.strip()

try:
    product = Product(name="", price=-10, quantity=5)
except ValidationError as e:
    print(e.errors())
```

### Advanced Models
```python
from pydantic import ConfigDict

class Config(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        json_schema_extra={
            "example": {
                "name": "John",
                "email": "john@example.com"
            }
        }
    )
    name: str
    email: str
```

## Testing with Pytest

### Basic Tests
```python
import pytest
from typing import List

def add(a: int, b: int) -> int:
    return a + b

def test_add_positive():
    assert add(2, 3) == 5

def test_add_negative():
    assert add(-2, -3) == -5

def test_add_zero():
    assert add(0, 0) == 0

# Run: pytest test_file.py -v
```

### Fixtures
```python
@pytest.fixture
def sample_data() -> List[int]:
    return [1, 2, 3, 4, 5]

@pytest.fixture
def database():
    # Setup
    db = {"connected": True}
    yield db
    # Teardown
    db["connected"] = False

def test_with_fixture(sample_data):
    assert len(sample_data) == 5

def test_with_db(database):
    assert database["connected"] is True
```

### Parameterized Tests
```python
@pytest.mark.parametrize("input,expected", [
    (2, 4),
    (3, 9),
    (4, 16),
])
def test_square(input, expected):
    assert input ** 2 == expected
```

### Mocking and Patching
```python
from unittest.mock import Mock, patch

def test_external_api(monkeypatch):
    mock_response = Mock()
    mock_response.json.return_value = {"status": "ok"}

    def mock_get(*args, **kwargs):
        return mock_response

    with patch('requests.get', mock_get):
        # Your code that calls requests.get
        pass
```

### Async Testing
```python
@pytest.mark.asyncio
async def test_async_function():
    result = await fetch_data("http://example.com")
    assert result is not None
```

## Virtual Environments

### Setup
```bash
# Create virtual environment
python -m venv venv

# Activate
# On Unix/macOS:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install packages
pip install fastapi pydantic pytest

# Create requirements.txt
pip freeze > requirements.txt

# Install from requirements.txt
pip install -r requirements.txt

# Deactivate
deactivate
```

### Poetry Alternative
```bash
# Initialize project
poetry init

# Add dependencies
poetry add fastapi pydantic pytest

# Install
poetry install

# Run
poetry run python main.py
```

## Best Practices

✅ **Use type hints** for all functions and variables
✅ **Virtual environments** for project isolation
✅ **Pydantic** for data validation
✅ **Async/await** for I/O-bound operations
✅ **Comprehensive tests** with pytest
✅ **Error handling** with proper exceptions
✅ **Logging** for debugging
✅ **Docstrings** for documentation
✅ **Code formatting** with Black or Ruff

## Common Pitfalls

❌ Missing type hints
❌ Not using virtual environments
❌ Blocking I/O in async functions
❌ Inadequate error handling
❌ No input validation
❌ Insufficient test coverage
❌ Mutable default arguments
❌ Not handling exceptions properly
❌ Circular imports

## Resources

- [Python Official Docs](https://docs.python.org/3/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)
- [Async Programming](https://docs.python.org/3/library/asyncio.html)

# JSON Response Examples

## List with Pagination

```json
{
  "success": true,
  "data": {
    "items": [
      {
        "itemId": 1,
        "name": "Item Example",
        "status": {
          "masterTableId": 10,
          "name": "ACTIVE",
          "value": "Active",
          "backgroundColor": "#22c55e",
          "textColor": "#ffffff"
        },
        "recordCreationDate": "2025-01-10T10:00:00-05:00"
      }
    ]
  },
  "message": "Items retrieved successfully",
  "pagination": {
    "page": 1,
    "pageSize": 10,
    "totalRecords": 25,
    "totalPages": 3,
    "hasNext": true,
    "hasPrevious": false
  }
}
```

## Detail

```json
{
  "success": true,
  "data": {
    "item": {
      "itemId": 1,
      "name": "Item Example",
      "description": "Item description",
      "status": {
        "masterTableId": 10,
        "name": "ACTIVE",
        "value": "Active"
      },
      "type": {
        "masterTableId": 20,
        "name": "TYPE_A",
        "value": "Type A"
      },
      "subItems": [
        { "subItemId": 1, "name": "Sub Item 1" }
      ]
    }
  },
  "message": "Item retrieved successfully"
}
```

## Validation Error

```json
{
  "success": false,
  "message": "Validation error",
  "errors": [
    { "code": "VAL_001", "field": "name", "message": "'Name' is required." },
    { "code": "VAL_002", "field": "email", "message": "'Email' is not a valid email." }
  ]
}
```

## Create Response

```json
{
  "success": true,
  "data": {
    "item": {
      "itemId": 42,
      "name": "New Item",
      "recordCreationDate": "2025-01-15T14:30:00-05:00"
    }
  },
  "message": "Item created successfully"
}
```

## Delete Response

```json
{
  "success": true,
  "data": {
    "id": 42
  },
  "message": "Item deleted successfully"
}
```

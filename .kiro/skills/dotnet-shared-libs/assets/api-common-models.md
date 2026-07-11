# API Common Models Reference
## Table of Contents
- [ApiResponse<T> (Generic)](#apiresponset-generic)
- [ApiResponse (Non-Generic)](#apiresponse-non-generic)
- [ApiError](#apierror)
- [PaginationResult](#paginationresult)
- [Exception Hierarchy](#exception-hierarchy)
- [CommonErrorCodes](#commonerrorcodes)
- [CommonErrorMessages](#commonerrormessages)
- [Cross-cutting Models](#cross-cutting-models)
- [IPagedRequest Interface](#ipagedrequest-interface)
- [PaginationDefaultsFilter](#paginationdefaultsfilter)
- [HeaderToken](#headertoken)
- [DictionaryExtensions](#dictionaryextensions)
- [IValidatableOptions](#ivalidatableoptions)

## ApiResponse<T> (Generic)
```csharp
public class ApiResponse<T>
{
    public bool Success { get; set; }
    public T? Data { get; set; }
    public string Message { get; set; } = string.Empty;
    public List<ApiError>? Errors { get; set; }
    public PaginationResult? Pagination { get; set; }
    public Dictionary<string, object>? Metadata { get; set; }
    public static ApiResponse<T> Ok(T data, string message = "Operación exitosa");
    public static ApiResponse<T> Ok(T data, PaginationResult pagination, string message = "Operación exitosa");
    public static ApiResponse<T> Ok(T data, Dictionary<string, object> metadata, string message = "Operación exitosa");
    public static ApiResponse<T> Ok(T data, PaginationResult pagination, Dictionary<string, object> metadata, string message = "Operación exitosa");
    public static ApiResponse<T> Fail(string message, List<ApiError> errors);
    public static ApiResponse<T> Fail(string message, ApiError error);
    public static ApiResponse<T> Fail(string code, string message, string? field = null);
}
```

## ApiResponse (Non-Generic)
```csharp
public class ApiResponse : ApiResponse<object>
{
    public static ApiResponse Ok(string message = "Operación exitosa");
    public new static ApiResponse Fail(string message, List<ApiError> errors);
    public new static ApiResponse Fail(string message, ApiError error);
    public static ApiResponse<ItemData<T>> OkItem<T>(T item, string message = "Operación exitosa");
    public static ApiResponse<ItemData<T>> OkItem<T>(T item, Dictionary<string, object> metadata, string message = "Operación exitosa");
    public static ApiResponse<ItemsData<T>> OkList<T>(List<T> items, string message = "Operación exitosa");
    public static ApiResponse<ItemsData<T>> OkList<T>(List<T> items, PaginationResult pagination, string message = "Operación exitosa");
    public static ApiResponse<ItemsData<T>> OkList<T>(List<T> items, Dictionary<string, object> metadata, string message = "Operación exitosa");
    public static ApiResponse<ItemsData<T>> OkList<T>(List<T> items, PaginationResult pagination, Dictionary<string, object> metadata, string message = "Operación exitosa");
}
```
> CRITICAL: `OkItem<T>()` and `OkList<T>()` live on non-generic `ApiResponse`, not on `ApiResponse<T>`.

## ApiError
```csharp
public sealed class ApiError
{
    public string Code { get; set; } = string.Empty;
    public string? Field { get; set; }
    public string Message { get; set; } = string.Empty;
    public ApiError();
    public ApiError(string code, string message, string? field = null);
    public static ApiError Validation(string code, string field, string message);
    public static ApiError General(string code, string message);
}
```

## PaginationResult
```csharp
public sealed class PaginationResult
{
    public int Page { get; set; }
    public int PageSize { get; set; }
    public int TotalRecords { get; set; }
    public int TotalPages { get; set; }
    public bool HasNext { get; set; }
    public bool HasPrevious { get; set; }
    public PaginationResult();
    public PaginationResult(int page, int pageSize, int totalRecords);
    public static PaginationResult Create(int page, int pageSize, int totalRecords);
}
```
Computed by constructor/factory: `TotalPages`, `HasNext`, `HasPrevious`.

## Exception Hierarchy
```csharp
public class BusinessException : Exception
{
    public string Code { get; }
    public string? Field { get; }
    public List<ApiError> Errors { get; }
    public BusinessException(string code, string message, string? field = null);
    public BusinessException(List<ApiError> errors);
    public ApiResponse<T> ToApiResponse<T>();
    public ApiResponse ToApiResponse();
}
public sealed class NotFoundException : BusinessException { public NotFoundException(string code, string message, string? field = null); }
public sealed class ValidationException : BusinessException { public ValidationException(string code, string message, string? field = null); public ValidationException(List<ApiError> errors); public ValidationException(List<string> messages); }
public sealed class ConflictException : BusinessException { public ConflictException(string code, string message, string? field = null); }
public sealed class ForbiddenException : BusinessException { public ForbiddenException(string code, string message, string? field = null); }
public sealed class BusinessRuleException : BusinessException { public BusinessRuleException(string code, string message, string? field = null); }
public sealed class BadGatewayException : BusinessException { public string? Details { get; } public BadGatewayException(string message, string? details = null); }
```

## CommonErrorCodes
18 public constants grouped by prefix:
- `VAL_`: `VAL_001`, `VAL_002`, `VAL_003`, `VAL_004`, `VAL_005`, `VAL_006`, `VAL_007`, `VAL_008`
- `AUTH_`: `AUTH_001`, `AUTH_002`, `AUTH_003`
- `PERM_`: `PERM_001`, `PERM_002`
- `SYS_`: `SYS_001`, `SYS_002`, `SYS_003`, `SYS_004`
- `FILE_`: `FILE_001`, `FILE_002`, `FILE_003`

## CommonErrorMessages
```csharp
public static class CommonErrorMessages
{
    public static string GetMessage(string code);
    public static string GetMessage(string code, string field);
    public static ApiError ToApiError(string code, string? field = null);
}
```
Behavior: `GetMessage(code)` returns mapped message or `"Error desconocido"`; overload appends `": {field}"`; `ToApiError` builds `new ApiError(code, GetMessage(code), field)`.

## Cross-cutting Models
```csharp
public class BaseAuditableEntity { public required string RecordCreationUser { get; set; } public required DateTimeOffset RecordCreationDate { get; set; } public string? RecordEditUser { get; set; } public DateTimeOffset? RecordEditDate { get; set; } public required string RecordStatus { get; set; } }
public class MasterTable { public int MasterTableId { get; set; } public string Name { get; set; } = string.Empty; public string Value { get; set; } = string.Empty; public string? AdditionalOne { get; set; } public string? AdditionalTwo { get; set; } public string? AdditionalThree { get; set; } }
public sealed class ItemData<T> { public T? Item { get; set; } public ItemData(); public ItemData(T item); }
public sealed class ItemsData<T> { public List<T> Items { get; set; } = []; public ItemsData(); public ItemsData(List<T> items); }
public class DocumentMetadataDto { public string FileName { get; set; } = string.Empty; public string? FileExtension { get; set; } public decimal? FileSizeKB { get; set; } public string FilePath { get; set; } = string.Empty; public string? ContentType { get; set; } }
```

## IPagedRequest Interface
```csharp
public interface IPagedRequest
{
    int Page { get; set; }
    int PageSize { get; set; }
    string? Search { get; set; }
    string? SortBy { get; set; }
    string? SortOrder { get; set; }
}
```

## PaginationDefaultsFilter
```csharp
public class PaginationDefaultsFilter : IEndpointFilter
{
    public PaginationDefaultsFilter(int maxPageSize = 50);
    public ValueTask<object?> InvokeAsync(EndpointFilterInvocationContext context, EndpointFilterDelegate next);
}
public static class EndpointFilterExtensions
{
    public static RouteHandlerBuilder WithPaginationDefaults(this RouteHandlerBuilder builder, int maxPageSize = 50);
}
```
Public behavior: requires `Page > 0` and `PageSize > 0` (otherwise `Results.BadRequest(...)`), caps `PageSize`, defaults `SortOrder` to `"DESC"`, uppercases non-empty `SortOrder`, and normalizes blank `Search`/`SortBy` to `null`.

## HeaderToken
`IEmployeeData` (getter-only `string?`) properties: `Guid`, `EmployeeId`, `CodTra`, `ProfileId`, `LastName`, `BirthName`, `FirstName`, `MiddleName`, `Gender`, `PhoneNumber`, `OnPremiseSamAccountName`, `UserPrincipalName`, `PositionCode`, `PositionDesc`, `AuthorityLevel`, `ManagerPersonId`, `EmployeeType`, `ModalidadId`, `Fiscalizado`, `Location`, `LocationDesc`, `CodCia`, `NomCia`, `Hierarchy`, `N1`, `N2`, `N3`, `N4`, `N5`, `N5Desc`, `VP`, `VPDesc`, `GerenciaSenior`, `GerenciaSeniorDesc`, `Gerencia`, `GerenciaDesc`, `Superintendencia`, `SuperintendenciaDesc`.
`IHeaderToken : IEmployeeData` adds getter-only `Token`, `Profile`, `Email`.
`EmployeeDataBase : IEmployeeData` exposes the same `IEmployeeData` property names with `get; set;`.

```csharp
public sealed class HeaderToken : EmployeeDataBase, IHeaderToken
{
    public string? Token { get; set; }
    public string? Profile { get; set; }
    public string? Email { get; set; }
}
public sealed class HappyUserResponse : EmployeeDataBase
{
    public string? Token { get; set; }
    public string? UserEdit { get; set; }
    public string? UserGuid { get; set; }
    public string? ActiveEmployeeId { get; set; }
    public string? ActiveCodtra { get; set; }
    public string? ActiveAuthorityLevel { get; set; }
    public string? ActiveEmail { get; set; }
    public bool IsReplacement { get; set; }
    public string? PublicIP { get; set; }
    public string? ClientIdentifier { get; set; }
    public string? Email { get; set; }
    public HeaderToken ToHeaderToken();
}
```

## DictionaryExtensions
```csharp
public static class DictionaryExtensions
{
    public static T? GetValue<T>(this IDictionary<string, object> dict, string key);
    public static T GetValueOrDefault<T>(this IDictionary<string, object> dict, string key, T defaultValue);
}
```

## IValidatableOptions
```csharp
public interface IValidatableOptions { void Validate(); }
```

# DictionaryMappingHelper

For mapping SP results with dot notation to nested objects.

## Helper Class

```csharp
public static class DictionaryMappingHelper
{
    public static T? GetValue<T>(IDictionary<string, object> dict, string key)
    {
        if (dict.TryGetValue(key, out var value) && value != null && value != DBNull.Value)
        {
            if (value is T typedValue) return typedValue;
            try { return (T)Convert.ChangeType(value, typeof(T)); }
            catch { return default; }
        }
        return default;
    }

    public static MasterTable? MapMasterTable(IDictionary<string, object> dict, string prefix)
    {
        var id = GetValue<int?>(dict, $"{prefix}.MasterTableId");
        if (id == null) return null;
        
        return new MasterTable
        {
            MasterTableId = id.Value,
            Name = GetValue<string>(dict, $"{prefix}.Name") ?? string.Empty,
            Value = GetValue<string>(dict, $"{prefix}.Value") ?? string.Empty,
            AdditionalOne = GetValue<string>(dict, $"{prefix}.AdditionalOne"),
            AdditionalTwo = GetValue<string>(dict, $"{prefix}.AdditionalTwo")
        };
    }

    public static StatusItem? MapStatusItem(IDictionary<string, object> dict, string prefix)
    {
        var id = GetValue<int?>(dict, $"{prefix}.MasterTableId");
        if (id == null) return null;
        
        return new StatusItem
        {
            MasterTableId = id.Value,
            Name = GetValue<string>(dict, $"{prefix}.Name") ?? string.Empty,
            Value = GetValue<string>(dict, $"{prefix}.Value") ?? string.Empty,
            BackgroundColor = GetValue<string>(dict, $"{prefix}.BackgroundColor"),
            TextColor = GetValue<string>(dict, $"{prefix}.TextColor"),
            Type = GetValue<string>(dict, $"{prefix}.Type")
        };
    }
}
```

## MappingProfile Usage

```csharp
public class {Entity}MappingProfile : Profile
{
    public {Entity}MappingProfile()
    {
        CreateMap<IDictionary<string, object>, {Entity}Item>()
            .ForMember(dest => dest.{Entity}Id, opt => opt.MapFrom(src => 
                DictionaryMappingHelper.GetValue<int>(src, "{Entity}Id")))
            .ForMember(dest => dest.Name, opt => opt.MapFrom(src => 
                DictionaryMappingHelper.GetValue<string>(src, "Name") ?? string.Empty))
            .ForMember(dest => dest.Status, opt => opt.MapFrom(src => 
                DictionaryMappingHelper.MapStatusItem(src, "Status")))
            .ForMember(dest => dest.Type, opt => opt.MapFrom(src => 
                DictionaryMappingHelper.MapMasterTable(src, "Type")));
    }
}
```

## Common Models

### MasterTable (Catalogs)

```csharp
public class MasterTable
{
    public int MasterTableId { get; set; }
    public string Name { get; set; } = string.Empty;
    public string Value { get; set; } = string.Empty;
    public string? AdditionalOne { get; set; }
    public string? AdditionalTwo { get; set; }
}
```

### StatusItem (Status with colors)

```csharp
public class StatusItem
{
    public int MasterTableId { get; set; }
    public string Name { get; set; } = string.Empty;
    public string Value { get; set; } = string.Empty;
    public string? BackgroundColor { get; set; }
    public string? TextColor { get; set; }
    public string? Type { get; set; }
}
```

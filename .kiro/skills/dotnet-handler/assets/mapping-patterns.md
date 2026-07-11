# Mapping Patterns

## Two Approaches

ANTA uses **two complementary mapping patterns**:

| Scenario | Pattern |
|----------|---------|
| List/Get with many fields | MappingProfile + AutoMapper |
| Create/Update simple response | DictionaryMappingHelper in handler |

---

## MappingProfile with Extension Method

Uses `src.GetValue<T>()` extension method from `ANTA.Shared.Common.Extensions`:

```csharp
using ANTA.Shared.Common.Extensions;
using ANTA.Shared.Common.Models;
using AutoMapper;

public class ListItemsMappingProfile : Profile
{
    public ListItemsMappingProfile()
    {
        CreateMap<IDictionary<string, object>, ListItemsItem>()
            .ForMember(dest => dest.ItemId, opt => opt.MapFrom(src => src["ItemId"]))
            .ForMember(dest => dest.Code, opt => opt.MapFrom(src => 
                src.GetValue<string>("Code") ?? string.Empty))
            .ForMember(dest => dest.Amount, opt => opt.MapFrom(src => src["Amount"]))
            
            .ForMember(dest => dest.Type, opt => opt.MapFrom(src =>
                src.GetValue<int?>("Type.MasterTableId") != null
                    ? new MasterTable
                    {
                        MasterTableId = src.GetValue<int>("Type.MasterTableId"),
                        Name = src.GetValue<string>("Type.Name") ?? string.Empty,
                        Value = src.GetValue<string>("Type.Value") ?? string.Empty,
                        AdditionalOne = src.GetValue<string>("Type.AdditionalOne"),
                        AdditionalTwo = src.GetValue<string>("Type.AdditionalTwo")
                    }
                    : null))
            
            .ForMember(dest => dest.Status, opt => opt.MapFrom(src =>
                src.GetValue<int?>("Status.MasterTableId") != null
                    ? new StatusItem
                    {
                        MasterTableId = src.GetValue<int>("Status.MasterTableId"),
                        Name = src.GetValue<string>("Status.Name") ?? string.Empty,
                        Value = src.GetValue<string>("Status.Value") ?? string.Empty,
                        BackgroundColor = src.GetValue<string>("Status.BackgroundColor"),
                        TextColor = src.GetValue<string>("Status.TextColor"),
                        Type = src.GetValue<string>("Status.Type")
                    }
                    : null))
            
            .ForMember(dest => dest.RecordCreationDate, opt => opt.MapFrom(src => 
                src.GetValue<DateTimeOffset?>("RecordCreationDate")));
    }
}
```

---

## DictionaryMappingHelper

Module-specific helper in `Modules/{Module}/Common/DictionaryMappingHelper.cs`:

```csharp
using ANTA.Shared.Common.Models;

namespace YourProject.Api.Modules.Items.Common;

public static class DictionaryMappingHelper
{
    public static StatusItem? MapStatus(IDictionary<string, object> dict, string prefix)
    {
        if (!dict.TryGetValue($"{prefix}.MasterTableId", out var id) || id == null || id == DBNull.Value)
            return null;

        return new StatusItem
        {
            MasterTableId = Convert.ToInt32(id),
            Name = GetString(dict, $"{prefix}.Name"),
            Value = GetString(dict, $"{prefix}.Value"),
            BackgroundColor = GetNullableString(dict, $"{prefix}.BackgroundColor"),
            TextColor = GetNullableString(dict, $"{prefix}.TextColor"),
            Type = GetNullableString(dict, $"{prefix}.Type")
        };
    }

    public static MasterTable? MapMasterTable(IDictionary<string, object> dict, string prefix)
    {
        if (!dict.TryGetValue($"{prefix}.MasterTableId", out var id) || id == null || id == DBNull.Value)
            return null;

        return new MasterTable
        {
            MasterTableId = Convert.ToInt32(id),
            Name = GetString(dict, $"{prefix}.Name"),
            Value = GetString(dict, $"{prefix}.Value"),
            AdditionalOne = GetNullableString(dict, $"{prefix}.AdditionalOne"),
            AdditionalTwo = GetNullableString(dict, $"{prefix}.AdditionalTwo")
        };
    }

    public static string GetString(IDictionary<string, object> dict, string key)
    {
        if (dict.TryGetValue(key, out var value) && value != null && value != DBNull.Value)
            return value.ToString() ?? string.Empty;
        return string.Empty;
    }

    public static string? GetNullableString(IDictionary<string, object> dict, string key)
    {
        if (dict.TryGetValue(key, out var value) && value != null && value != DBNull.Value)
            return value.ToString();
        return null;
    }
}
```

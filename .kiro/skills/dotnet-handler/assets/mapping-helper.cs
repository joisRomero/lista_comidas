public static class DictionaryMappingHelper
{
    public static T? GetValue<T>(IDictionary<string, object> dict, string key)
    {
        if (dict.TryGetValue(key, out var value) && value != null && value != DBNull.Value)
        {
            if (value is T typedValue)
                return typedValue;
            try
            {
                return (T)Convert.ChangeType(value, typeof(T));
            }
            catch
            {
                return default;
            }
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
            TextColor = GetValue<string>(dict, $"{prefix}.TextColor")
        };
    }
}

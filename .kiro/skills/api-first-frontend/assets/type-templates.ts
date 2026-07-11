export interface StatusItem {
  masterTableId: number;
  name: string;
  value: string;
  backgroundColor?: string | null;
  textColor?: string | null;
}

export interface MasterTableItem {
  masterTableId: number;
  name: string;
  value: string;
}

export interface PaginationResponse {
  page: number;
  pageSize: number;
  totalRecords: number;
  totalPages: number;
}

export interface ApiErrorItem {
  code: string;
  field: string | null;
  message: string;
}

export interface SubEntityItem {
  subEntityId: number;
  order: number;
}

export interface EntityListItem {
  entityId: number;
  code: string;
  name: string;
  status: StatusItem;
}

export interface EntitiesQueryParams extends Record<string, unknown> {
  page?: number;
  pageSize?: number;
  search?: string | null;
  statusId?: number | null;
  sortBy?: string | null;
  sortOrder?: string | null;
}

export interface EntitiesResponse {
  success: boolean;
  data: { items: EntityListItem[] };
  pagination: PaginationResponse;
  message: string;
}

export interface EntityDetail extends EntityListItem {
  subEntities: SubEntityItem[];
  summary: {
    totalSubEntities: number;
    totalAmount: number;
  };
}

export interface EntityResponse {
  success: boolean;
  data: { item: EntityDetail };
  message: string;
}

export interface CreateEntityRequest extends Record<string, unknown> {
  name: string;
  fieldId: number;
  subEntities?: { subEntityId: number; order: number }[];
}

export interface CreateEntityResponse {
  success: boolean;
  data: { item: { entityId: number; code: string; name: string; status: StatusItem } };
  message: string;
}

export interface UpdateEntityRequest extends Record<string, unknown> {
  name?: string;
  fieldId?: number;
}

export interface UpdateEntityResponse {
  success: boolean;
  data: { item: { entityId: number; name: string; status: StatusItem } };
  message: string;
}

export interface DeleteEntityResponse {
  success: boolean;
  data: { result: string; deletedEntityId: number; deletedCode: string; message: string };
  message: string;
}

export interface VerbEntityRequest extends Record<string, unknown> {
  optionalField?: string | null;
}

export interface VerbEntityResponse {
  success: boolean;
  data: {
    item: {
      entityId: number;
      code: string;
      status: StatusItem;
      transitionDate?: string | null;
    };
  };
  message: string;
}

export interface RemoveSubEntityRequest extends Record<string, unknown> {
  justification: string;
}

export interface RemoveSubEntityResponse {
  success: boolean;
  data: { result: string; removedSubEntityId: number; remainingCount: number; message: string };
  message: string;
}

export interface ReorderSubEntitiesRequest extends Record<string, unknown> {
  items: { subEntityId: number; order: number }[];
}

export interface ReorderSubEntitiesResponse {
  success: boolean;
  data: { items: { subEntityId: number; order: number }[] };
  message: string;
}

export interface SearchEntityParams extends Record<string, unknown> {
  search?: string | null;
  limit?: number;
}

export interface SearchEntityResponse {
  success: boolean;
  data: { items: EntityListItem[] };
  message: string;
}

export interface ApiErrorResponse {
  success: false;
  message: string;
  errors: ApiErrorItem[];
}

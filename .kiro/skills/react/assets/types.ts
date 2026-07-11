export interface ResponseApi<T> {
  success: boolean;
  data: T;
  message: string;
  errors: Array<{
    code: string | null;
    field: string | null;
    message: string | null;
  }> | null;
  pagination: {
    page: number;
    pageSize: number;
    totalRecords: number;
    totalPages: number;
    hasNext: boolean;
    hasPrevious: boolean;
  } | null;
  metadata: Record<string, unknown> | null;
}

export interface MasterTableItem {
  masterTableId: number;
  name: string | null;
  value: string | null;
  additionalOne: string | null;
  additionalTwo: string | null;
}

export interface StatusItem {
  masterTableId: number;
  name: string;
  value: string;
  backgroundColor: string | null;
  textColor: string | null;
  type: string | null;
}

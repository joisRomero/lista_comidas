// lib/errors/handler.ts - Centralized error handling

interface ApiErrorType {
  status: number;
  message: string;
}

type ErrorContext = {
  type?: 'api' | 'network' | 'remote';
  name?: string;
  component?: string;
};

const isApiError = (error: unknown): error is ApiErrorType => {
  return typeof error === 'object' && error !== null && 'status' in error;
};

export const handleError = (error: unknown, context?: ErrorContext) => {
  // Log error
  logger.error('Error logged:', { ...context, error });

  // Remote errors
  if (context?.type === 'remote') {
    toast.error(`${context.name || 'Módulo remoto'} no está disponible`);
    return;
  }

  // Network errors
  if (context?.type === 'network' || 
      (error instanceof TypeError && error.message.includes('fetch'))) {
    toast.error('Error de conexión. Verifica tu internet.');
    return;
  }

  // API errors
  if (isApiError(error)) {
    switch (error.status) {
      case 400: toast.error(error.message || 'Solicitud inválida'); break;
      case 401: toast.error('Sesión expirada'); break;
      case 403: toast.error('No tienes permisos para esta acción'); break;
      case 404: toast.error('Recurso no encontrado'); break;
      case 500: toast.error('Error interno del servidor'); break;
      default: toast.error(error.message || 'Error en la petición');
    }
  } else if (error instanceof Error) {
    toast.error(error.message);
  } else {
    toast.error('Ha ocurrido un error inesperado');
  }
};

// ---------------------------------------------------------------------------
// withRetry - Auto-retry with exponential backoff

export const withRetry = async <T>(
  fn: () => Promise<T>,
  maxRetries = 3,
  delay = 1000,
): Promise<T> => {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      // Don't retry business errors (401, 403, 404)
      if (isApiError(error) && [401, 403, 404].includes(error.status)) {
        throw error;
      }
      await new Promise((resolve) => setTimeout(resolve, delay * (i + 1)));
    }
  }
  throw new Error('Max retries exceeded');
};

// ---------------------------------------------------------------------------
// useConfirm - Modal confirmation hook

import { App } from 'antd';

export const useConfirm = () => {
  const { modal } = App.useApp();
  return modal.confirm;
};

// Usage:
// const confirm = useConfirm();
// confirm({
//   title: '¿Eliminar registro?',
//   content: 'Esta acción no se puede deshacer',
//   okText: 'Eliminar',
//   okType: 'danger',
//   cancelText: 'Cancelar',
//   onOk: () => remove(id),
// });

// ---------------------------------------------------------------------------
// useErrorHandler - Unified hook

import { handleError, withRetry } from '@/lib/errors/handler';

export const useErrorHandler = () => {
  return {
    handleError,
    executeWithRetry: withRetry,
  };
};

// ---------------------------------------------------------------------------
// Usage in Mutations

// addMutation.mutate(data, {
//   onError: (error) => handleError(error, { component: 'AddUser' }),
// });
//
// // With retry
// await withRetry(() => apiCall(), 3, 1000);

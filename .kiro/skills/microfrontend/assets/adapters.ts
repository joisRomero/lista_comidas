// shared/adapters/useHostApi.ts
import { createServiceMutation, createServiceQuery, createServiceBlobMutation } from 'host/factories';

export const useHostServiceQuery = () => createServiceQuery;
export const useHostServiceMutation = () => createServiceMutation;
export const useHostServiceBlobMutation = () => createServiceBlobMutation;

// shared/adapters/useHostAuth.ts
import { useSession } from 'host/session';

export const useHostAuth = () => useSession();

// shared/adapters/index.ts
export { useHostServiceQuery, useHostServiceMutation, useHostServiceBlobMutation } from './useHostApi';
export { useHostAuth } from './useHostAuth';
export { toast } from 'host/toast';
export { logger } from 'host/logger';

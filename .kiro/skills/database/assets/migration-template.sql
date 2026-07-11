/* ==============================================================================
-- Migration: YYYYMMDD_{Description}
-- Description: Brief description of the change
-- Author:      Author Name
-- Created:     YYYY-MM-DD
-- ============================================================================== */

-- Check if already applied (idempotent)
IF NOT EXISTS (
    SELECT 1 FROM {Table} WHERE {Condition}
)
BEGIN
    PRINT 'Applying migration: {Description}...';

    -- Migration logic here
    
    PRINT 'Migration completed successfully.';
END
ELSE
BEGIN
    PRINT 'Migration already applied. Skipping.';
END
GO

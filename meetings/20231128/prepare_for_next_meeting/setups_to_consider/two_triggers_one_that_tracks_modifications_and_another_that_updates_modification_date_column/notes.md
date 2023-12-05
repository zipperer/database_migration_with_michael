Suppose we want to track two separate event types:
 - for any edit to TABLE, update TABLE.modification_date to time of edit
 - for any edit to TABLE, record the edit somewhere

The approach below tracks both.

## for any edit to TABLE, update TABLE.modification_date to time of edit

Two steps:
 - create FUNCTION
 - create TRIGGER that uses function

### create FUNCTION

```SQL
-- https://stackoverflow.com/a/26284695
-- https://aviyadav231.medium.com/automatically-updating-a-timestamp-column-in-postgresql-using-triggers-98766e3b47a0
CREATE FUNCTION update_column_with_timestamp_1()
RETURNS TRIGGER AS $$
BEGIN
    NEW.column_that_tracks_modifications = now();
    RETURN NEW;
END;
$$ language 'plpgsql';
```

name `update_column_with_timestamp_1` is our choice.

`NEW` is plpgsql syntax for the new row.

name `column_that_tracks_modifications` is the name of our column that tracks the modification date.

`now()` is the value to which we are setting the entry in column `column_that_tracks_modifications`.

### create TRIGGER that uses function

```SQL
CREATE TRIGGER update_column_with_timestamp
BEFORE INSERT OR UPDATE OR DELETE ON public.example_table_with_column_that_tracks_modifications
FOR EACH ROW EXECUTE PROCEDURE update_column_with_timestamp_1();
```
Based on my experiments `BEFORE` works and `AFTER` does not.

name `update_column_with_timestamp` is our choice.

have not checked whether schema prefix `public.` required on name of table.

`update_column_with_timestamp_1()` is the name of the function we created with `CREATE FUNCTION` followed by `()`.

## for any edit to TABLE, record the edit somewhere

* https://dba.stackexchange.com/a/331380
* https://www.cybertec-postgresql.com/en/tracking-changes-in-postgresql/

Two steps:
 - create FUNCTION
 - create TRIGGER that uses function

### create FUNCTION

Aside: I encountered limitations due to privileges. I executed below with user postgres. Then for andrew_user to be able to see it I had to
```SQL
psql> GRANT ALL PRIVILEGES ON SCHEMA logging to andrew_user;
```
End Aside

```SQL
CREATE SCHEMA logging;

CREATE TABLE logging.t_history (
        id              serial,
        tstamp          timestamp       DEFAULT now(),
        schemaname      text,
        tabname         text,
        operation       text,
        who             text            DEFAULT current_user,
        new_val         jsonb,
        old_val         jsonb
);

CREATE FUNCTION logging.change_trigger() RETURNS trigger AS $$
BEGIN
INSERT INTO logging.t_history (tabname, schemaname, operation, new_val, old_val)
VALUES (TG_RELNAME, TG_TABLE_SCHEMA, TG_OP, pg_catalog.row_to_json(NEW), pg_catalog.row_to_json(OLD));
RETURN NULL;
END;
$$ LANGUAGE 'plpgsql' SECURITY DEFINER
SET search_path = pg_catalog,pg_temp;
```

### create TRIGGER that uses function

```SQL
CREATE TRIGGER audit_important_table
AFTER INSERT OR UPDATE OR DELETE ON important_table
FOR EACH ROW EXECUTE PROCEDURE logging.change_trigger();
```

edit name `important_table` to name for our table, e.g. `public.example_table_with_column_that_tracks_modifications`.
edit name `audit_important_table` to name of our choice, e.g. `audit_public_example_table_with_column_that_tracks_modifications`.


## aside: how to check which triggers are active?

https://stackoverflow.com/questions/704270/how-can-you-tell-if-a-trigger-is-enabled-in-postgresql

```SQL
SELECT pg_namespace.nspname, pg_class.relname, pg_trigger.*
FROM pg_trigger
JOIN pg_class ON pg_trigger.tgrelid = pg_class.oid
JOIN pg_namespace ON pg_namespace.oid = pg_class.relnamespace
```

If `tgenabled` is `'D'`, the trigger is disabled. All other values (documented here) indicate, that it is enabled in some way.

## drop trigger and drop function

While experimenting, I have 'reset' the state of the database by:
 - drop trigger
 - drop function
 - redefine function
 - redefine trigger
e.g.

```SQL
postgres=# DROP TRIGGER update_column_with_timestamp ON public.example_table_with_column_that_tracks_modifications;
DROP TRIGGER
postgres=# DROP FUNCTION update_timestamp_trigger;
DROP FUNCTION
postgres=# CREATE FUNCTION update_timestamp_trigger() ...
CREATE FUNCTION
postgres=# CREATE TRIGGER update_column_with_timestamp ...
CREATE TRIGGER
```

## perform experiment
 - create new database and table
 - table includes column that tracks modification time with timestamp
 - add these functions and triggers
 - confirm works

For psql interactions, see files with name `psql-interactions-...{original,clean}.txt` in this folder.

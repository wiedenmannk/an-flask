--
-- PostgreSQL database dump
--

-- Dumped from database version 14.13 (Ubuntu 14.13-0ubuntu0.22.04.1)
-- Dumped by pg_dump version 15.1 (Ubuntu 15.1-1.pgdg20.04+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: public; Type: SCHEMA; Schema: -; Owner: postgres
--

-- *not* creating schema, since initdb creates it


ALTER SCHEMA public OWNER TO postgres;

--
-- Name: fn_extractdatafrommodel_tv(); Type: FUNCTION; Schema: public; Owner: root
--

CREATE FUNCTION public.fn_extractdatafrommodel_tv() RETURNS TABLE("TableName" character varying, "KeyType" character, "ColumnName" character varying, "DataType" character varying, "SortOrder" integer)
    LANGUAGE plpgsql
    AS $$
BEGIN
	RETURN QUERY

	WITH RECURSIVE db_objects 
	AS 
	(
		WITH CTE_XmlExport (id,	value,	parent,	rownum)
		AS
		(
			SELECT
				id,
				value,
				parent,
				rownum
			FROM
			(
				SELECT 
				     (xpath('//@id', myTempTable.myXmlColumn))[1]::text AS id
				    ,(xpath('//@value', myTempTable.myXmlColumn))[1]::text AS value 
				    ,(xpath('//@parent', myTempTable.myXmlColumn))[1]::text AS parent
				    ,myTempTable.myXmlColumn as myXmlElement
					,ROW_NUMBER() OVER () AS rownum
				FROM unnest(
				    xpath
				    (    '//mxCell'
				        ,XMLPARSE(DOCUMENT convert_from(pg_read_binary_file('/db_model/db_model.drawio.xml'), 'UTF8'))
				    )
				) AS myTempTable(myXmlColumn)
			) AS leckmich
		)
		SELECT 
			value as TableName,
			id,
			parent,
			value,
			rownum
		FROM CTE_XmlExport
		WHERE parent = '1'
		UNION ALL 
		SELECT
			TableName,
			CTE_XmlExport.id,
			CTE_XmlExport.parent,
			CTE_XmlExport.value,
			CTE_XmlExport.rownum
		FROM CTE_XmlExport 
	
		INNER JOIN db_objects 
			ON CTE_XmlExport.parent  = db_objects.id
	)
	SELECT
		CAST(tablename AS varchar(255)) AS tablename
		,CAST(CASE WHEN COALESCE(col3,'') = '' THEN '' ELSE col1 END AS char(2)) AS KeyType
		,CAST(CASE WHEN COALESCE(col3,'') = '' THEN col1 ELSE col2 END AS varchar(255))  AS ColumnName
		,CAST(CASE WHEN COALESCE(col3,'') = '' THEN col2 ELSE col3 END AS varchar(255))  AS datatype
		,CAST(ROW_NUMBER() OVER (Partition BY tablename ORDER BY min_row) AS int) AS SortOrder
	FROM
	(
		SELECT
			tablename,
			min_row,
			split_part(value,' ',1) as col1, 
			split_part(value,' ',2) as col2, 
			split_part(value,' ',3) as col3 
		FROM
		(
			SELECT 
				tablename,
				parent,
				MIN(rownum) as min_row,
				STRING_AGG(value,' ' ORDER BY id ASC) as value
			FROM db_objects
			WHERE COALESCE(value,'') <> ''
			AND parent <> '1'
			GROUP BY tablename,parent
			ORDER BY TableName,parent
		) AS leckmich2	
	) AS leckmich3
	WHERE tablename IS NOT NULL
	ORDER BY min_row;	
END;
$$;


ALTER FUNCTION public.fn_extractdatafrommodel_tv() OWNER TO root;

--
-- Name: fn_extracttabledatafrommodel_tv(character varying); Type: FUNCTION; Schema: public; Owner: root
--

CREATE FUNCTION public.fn_extracttabledatafrommodel_tv(extracttablename character varying) RETURNS TABLE("TableName" character varying, "KeyType" character, "ColumnName" character varying, "DataType" character varying, "SortOrder" integer)
    LANGUAGE plpgsql
    AS $$
BEGIN
	RETURN QUERY

	WITH RECURSIVE db_objects 
	AS 
	(
		WITH CTE_XmlExport (id,	value,	parent,	rownum)
		AS
		(
			SELECT
				id,
				value,
				parent,
				rownum
			FROM
			(
				SELECT 
				     (xpath('//@id', myTempTable.myXmlColumn))[1]::text AS id
				    ,(xpath('//@value', myTempTable.myXmlColumn))[1]::text AS value 
				    ,(xpath('//@parent', myTempTable.myXmlColumn))[1]::text AS parent
				    ,myTempTable.myXmlColumn as myXmlElement
					,ROW_NUMBER() OVER () AS rownum
				FROM unnest(
				    xpath
				    (    '//mxCell'
				        ,XMLPARSE(DOCUMENT convert_from(pg_read_binary_file('/db_model/db_model.drawio.xml'), 'UTF8'))
				    )
				) AS myTempTable(myXmlColumn)
			) AS xmlColumn
		)
		SELECT 
			value as TableName,
			id,
			parent,
			value,
			rownum
		FROM CTE_XmlExport
		WHERE parent = '1'
		AND value = ExtractTableName
		UNION ALL 
		SELECT
			TableName,
			CTE_XmlExport.id,
			CTE_XmlExport.parent,
			CTE_XmlExport.value,
			CTE_XmlExport.rownum
		FROM CTE_XmlExport 
	
		INNER JOIN db_objects 
			ON CTE_XmlExport.parent  = db_objects.id
		WHERE TableName = ExtractTableName
	)
	SELECT
		CAST(tablename AS varchar(255)) AS tablename
		,CAST(CASE WHEN COALESCE(col3,'') = '' THEN '' ELSE col1 END AS char(2)) AS KeyType
		,CAST(CASE WHEN COALESCE(col3,'') = '' THEN col1 ELSE col2 END AS varchar(255))  AS ColumnName
		,CAST(CASE WHEN COALESCE(col3,'') = '' THEN col2 ELSE col3 END AS varchar(255))  AS datatype
		,CAST(ROW_NUMBER() OVER (Partition BY tablename ORDER BY min_row) AS int) AS SortOrder
	FROM
	(
		SELECT
			tablename,
			min_row,
			split_part(value,' ',1) as col1, 
			split_part(value,' ',2) as col2, 
			split_part(value,' ',3) as col3 
		FROM
		(
			SELECT 
				tablename,
				parent,
				MIN(rownum) as min_row,
				STRING_AGG(value,' ' ORDER BY id ASC) as value
			FROM db_objects
			WHERE COALESCE(value,'') <> ''
			AND parent <> '1'
			GROUP BY tablename,parent
			ORDER BY TableName,parent
		) AS Tablesspooler	
	) AS lassmich
	WHERE tablename IS NOT NULL
	ORDER BY min_row;	
END;
$$;


ALTER FUNCTION public.fn_extracttabledatafrommodel_tv(extracttablename character varying) OWNER TO root;

--
-- Name: fn_getcreatetableddl_sv(character varying, character varying); Type: FUNCTION; Schema: public; Owner: root
--

CREATE FUNCTION public.fn_getcreatetableddl_sv(createtableschemaname character varying, createtablename character varying) RETURNS text
    LANGUAGE plpgsql
    AS $_$
DECLARE
	CreateTableDdl text;
BEGIN
	SELECT
	CONCAT(
	'CREATE TABLE "',CreateTableSchemaName,'"."',CreateTableName,'"
	 (',
	  "ColumnDefinition",
	 ',CONSTRAINT "',CreateTableName,'_pk" PRIMARY KEY (',"PrimaryKeyDefinition",'))') 
	 INTO CreateTableDdl
	FROM
	(
	    SELECT 
				STRING_AGG(CONCAT('"',"ColumnName", '" ', "DataType" , ' ' , CASE WHEN "KeyType" = 'PK' THEN ' NOT NULL' ELSE ' NULL' END) ,', ' ORDER BY "SortOrder" ASC) AS "ColumnDefinition",
			REGEXP_REPLACE(STRING_AGG(CONCAT(CASE WHEN "KeyType" = 'PK' THEN CONCAT ('"',"ColumnName",'"') ELSE NULL END) ,', ' ORDER BY "SortOrder" ASC), '[ ,]*$', ' ') AS "PrimaryKeyDefinition"
		FROM (SELECT (fn_ExtractTableDataFromModel_Tv(CreateTableName)).*) AS extractor
	) AS nimmmichmit;
	RETURN CreateTableDdl;
END;
$_$;


ALTER FUNCTION public.fn_getcreatetableddl_sv(createtableschemaname character varying, createtablename character varying) OWNER TO root;

--
-- Name: fn_getinserttabledml_sv(character varying, character varying); Type: FUNCTION; Schema: public; Owner: root
--

CREATE FUNCTION public.fn_getinserttabledml_sv(createtableschemaname character varying, createtablename character varying) RETURNS text
    LANGUAGE plpgsql
    AS $$
DECLARE
	InsertTableDml text;
BEGIN
	
	SELECT 
		CONCAT
		(
			'INSERT INTO "',CreateTableSchemaName,'"."',CreateTableName,'" (',ColumnList,')
			 SELECT ',ColumnList,' FROM "',CreateTableSchemaName,'"."',CreateTableName,'_Bac"' 
		)
	INTO InsertTableDml
	FROM
	(
		SELECT
		STRING_AGG(CONCAT('"',Column_name,'"'),', ') as ColumnList
		FROM
		(
			SELECT Column_name FROM information_schema.columns WHERE table_schema= CreateTableSchemaName AND table_name = CreateTableName
			INTERSECT
			SELECT Column_name FROM information_schema.columns WHERE table_schema= CreateTableSchemaName AND table_name = CONCAT(CreateTableName,'_Bac') 
		) GetColumns
	) GetColumnList	;
	RETURN InsertTableDml;
END;
$$;


ALTER FUNCTION public.fn_getinserttabledml_sv(createtableschemaname character varying, createtablename character varying) OWNER TO root;

--
-- Name: sp_createtable_ddl(character varying, character varying); Type: PROCEDURE; Schema: public; Owner: root
--

CREATE PROCEDURE public.sp_createtable_ddl(IN tab_schema character varying DEFAULT 'Weltherrschaft'::character varying, IN tab character varying DEFAULT ''::character varying)
    LANGUAGE plpgsql
    AS $$
DECLARE
	
    colnames VARCHAR(255)[];
	i VARCHAR(255);
	sql_CreateTable text;
	sql_DropTable text;
	sql_getRowCount text;
	sql_CopyTable text;
	sql_InsertTable text;
	TabRowCount int;
	BEGIN
		

		IF COALESCE(tab,'') <> '' THEN
			colnames := ARRAY(
		    SELECT tab
			);
		ELSE
			colnames := ARRAY(
			    SELECT "TableName"
			    FROM (SELECT DISTINCT(fn_ExtractDataFromModel_Tv())."TableName") AS FN_EXTRACTOR
			
				);
		END IF;

		FOREACH i IN ARRAY colnames
		LOOP
			SELECT CONCAT('DROP TABLE "',tab_schema,'"."',i,'"') INTO sql_DropTable;
			IF EXISTS (
			   SELECT FROM information_schema.tables 
			   WHERE  table_schema = tab_schema
			   AND    table_name   = i
			   ) THEN
					SELECT CONCAT('SELECT COUNT(*) FROM "',tab_schema,'"."',i,'"') INTO sql_getRowCount;
					EXECUTE sql_getRowCount INTO TabRowCount;
							
					IF COALESCE(TabRowCount,0) > 0 THEN

						RAISE NOTICE '%','CopyTable';
						SELECT CONCAT('CREATE TABLE "',tab_schema,'"."',i,'_Bac" AS TABLE "',tab_schema,'"."',i,'";') INTO sql_CopyTable;
						RAISE NOTICE '%',sql_CopyTable;
						EXECUTE sql_CopyTable;
					END IF;
				RAISE NOTICE '%','DropTable';
				RAISE NOTICE '%',sql_DropTable;
				EXECUTE sql_DropTable;
			END IF;
			sql_CreateTable := fn_GetCreateTableDdl_Sv(tab_schema,i);
			RAISE NOTICE '%','CreateTable';
			RAISE NOTICE '%',sql_CreateTable;
			EXECUTE sql_CreateTable;

			IF EXISTS (
			   SELECT FROM information_schema.tables 
			   WHERE  table_schema = tab_schema
			   AND    table_name   = CONCAT(i,'_Bac')
			   ) THEN
				sql_InsertTable := fn_GetInsertTableDml_Sv(tab_schema,i);
			  	RAISE NOTICE '%','InsertTable';
				RAISE NOTICE '%',sql_InsertTable;
				EXECUTE sql_InsertTable;
			END IF;
			
		END LOOP;
	END
$$;


ALTER PROCEDURE public.sp_createtable_ddl(IN tab_schema character varying, IN tab character varying) OWNER TO root;

--
-- Name: sp_deletebactable_ddl(character varying); Type: PROCEDURE; Schema: public; Owner: root
--

CREATE PROCEDURE public.sp_deletebactable_ddl(IN tab_schema character varying DEFAULT 'Weltherrschaft'::character varying)
    LANGUAGE plpgsql
    AS $$
DECLARE
	
    colnames VARCHAR(255)[];
	i VARCHAR(255);
	sql_DropTable text;
	BEGIN
		
		colnames := ARRAY(
		   SELECT table_name FROM information_schema.tables WHERE table_schema = tab_schema AND RIGHT(table_name,4) = '_Bac'
		);
		
		FOREACH i IN ARRAY colnames
		LOOP
			SELECT CONCAT('DROP TABLE "',tab_schema,'"."',i,'"') INTO sql_DropTable;
			RAISE NOTICE '%','DropTable';
			RAISE NOTICE '%',sql_DropTable;
			EXECUTE sql_DropTable;
		END LOOP;
	END
$$;


ALTER PROCEDURE public.sp_deletebactable_ddl(IN tab_schema character varying) OWNER TO root;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: Bank; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public."Bank" (
    "Bank_ID" integer NOT NULL,
    "BankIdentifierCode" character varying(32)
);


ALTER TABLE public."Bank" OWNER TO root;

--
-- Name: BankMultilingual; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public."BankMultilingual" (
    "Bank_ID" bigint NOT NULL,
    "Language_ID" integer NOT NULL,
    "Name" character varying(255),
    "Description" character varying(1000)
);


ALTER TABLE public."BankMultilingual" OWNER TO root;

--
-- Name: City; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public."City" (
    "City_ID" integer NOT NULL,
    "ZipCode" character varying(16),
    "State_ID" integer
);


ALTER TABLE public."City" OWNER TO root;

--
-- Name: CityMultilingual; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public."CityMultilingual" (
    "City_ID" bigint NOT NULL,
    "Language_ID" integer NOT NULL,
    "Name" character varying(255),
    "Description" character varying(1000)
);


ALTER TABLE public."CityMultilingual" OWNER TO root;

--
-- Name: Company; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public."Company" (
    "Company_ID" bigint NOT NULL,
    "CompanyName" character varying(255),
    "Sex_ID" bigint,
    "FirstName" character varying(255),
    "LastName" character varying(255),
    "Street" character varying(255),
    "City_ID" integer,
    "EmailAddress" character varying(255),
    "TelefoneNumber" character varying(255),
    "MobileNumber" character varying(255),
    "Language_ID" integer,
    "BankAccountOwner" character varying(64),
    "Bank_ID" integer,
    "InternationalBankAccountNumber" character varying(32),
    "TaxNumber" character varying(32),
    "Currency_ID" integer,
    "ChangedAt" timestamp without time zone
);


ALTER TABLE public."Company" OWNER TO root;

--
-- Name: Country; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public."Country" (
    "Country_ID" integer NOT NULL,
    "CountryCode" character varying(16),
    "Currency_ID" integer,
    "Official_Language_ID" integer
);


ALTER TABLE public."Country" OWNER TO root;

--
-- Name: CountryMultilingual; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public."CountryMultilingual" (
    "Country_ID" bigint NOT NULL,
    "Language_ID" integer NOT NULL,
    "Name" character varying(255),
    "Description" character varying(1000)
);


ALTER TABLE public."CountryMultilingual" OWNER TO root;

--
-- Name: Currency; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public."Currency" (
    "Currency_ID" integer NOT NULL,
    "CurrencyCode" character varying(16)
);


ALTER TABLE public."Currency" OWNER TO root;

--
-- Name: CurrencyExchange; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public."CurrencyExchange" (
    "Currency_ID" integer NOT NULL,
    "Exchange_Currency_ID" integer,
    "ExchangeRate" numeric(12,4)
);


ALTER TABLE public."CurrencyExchange" OWNER TO root;

--
-- Name: Customer; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public."Customer" (
    "Customer_ID" bigint NOT NULL,
    "CompanyName" character varying(255),
    "Company_ID" bigint,
    "Sex_ID" smallint,
    "Language_ID" integer,
    "FirstName" character varying(255),
    "LastName" character varying(255),
    "Street" character varying(255),
    "City_ID" integer,
    "EmailAddress" character varying(255),
    "TelefoneNumber" character varying(255),
    "MobileNumber" character varying(255),
    "CustomerCode" character varying(255),
    "ChangedAt" timestamp without time zone
);


ALTER TABLE public."Customer" OWNER TO root;

--
-- Name: Date; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public."Date" (
    "Date_ID" bigint NOT NULL,
    "DateCode" character varying(255),
    "Month_ID" bigint,
    "Year_ID" integer,
    "Quarter_ID" integer
);


ALTER TABLE public."Date" OWNER TO root;

--
-- Name: InvoiceHeader; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public."InvoiceHeader" (
    "Invoice_ID" bigint NOT NULL,
    "InvoiceNumber" character varying(255),
    "Create_Date_ID" bigint,
    "Invoice_Date_ID" bigint,
    "Company_ID" bigint,
    "Currency_ID" integer,
    "Customer_ID" bigint,
    "Language_ID" integer,
    "DiscountDays" integer,
    "PaymentTerminInDays" integer,
    "ChangedAt" timestamp without time zone,
    "Discount" numeric(4,2)
);


ALTER TABLE public."InvoiceHeader" OWNER TO root;

--
-- Name: InvoicePosition; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public."InvoicePosition" (
    "Invoice_ID" bigint NOT NULL,
    "PositionNumber" integer,
    "Product_ID" bigint,
    "Quantity" integer,
    "SalesPrice" numeric(18,2),
    "ChangedAt" timestamp without time zone
);


ALTER TABLE public."InvoicePosition" OWNER TO root;

--
-- Name: Language; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public."Language" (
    "Language_ID" integer NOT NULL,
    "LanguageCode" character varying(2)
);


ALTER TABLE public."Language" OWNER TO root;

--
-- Name: Product; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public."Product" (
    "Product_ID" integer NOT NULL,
    "Company_ID" integer,
    "ProductCode" character varying(16),
    "Unit_ID" integer,
    "ProductGroup_ID" integer,
    "ListPrice" numeric(18,2),
    "Active_FLAG" bit(1),
    "ChangedAt" timestamp without time zone
);


ALTER TABLE public."Product" OWNER TO root;

--
-- Name: ProductGroup; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public."ProductGroup" (
    "ProducrGroup_ID" integer NOT NULL,
    "ProductGroupCode" character varying(16)
);


ALTER TABLE public."ProductGroup" OWNER TO root;

--
-- Name: ProductGroupMultilingual; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public."ProductGroupMultilingual" (
    "ProductGroup_ID" integer NOT NULL,
    "Language_ID" integer NOT NULL,
    "Name" character varying(255),
    "Description" character varying(1000)
);


ALTER TABLE public."ProductGroupMultilingual" OWNER TO root;

--
-- Name: ProductGroupVat; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public."ProductGroupVat" (
    "Vat_ID" integer NOT NULL,
    "ProductGroup_ID" integer NOT NULL,
    "State_ID" integer,
    "Country_ID" integer
);


ALTER TABLE public."ProductGroupVat" OWNER TO root;

--
-- Name: ProductMultilingual; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public."ProductMultilingual" (
    "Product_ID" bigint NOT NULL,
    "Language_ID" integer NOT NULL,
    "Name" character varying(255),
    "Description" character varying(1000)
);


ALTER TABLE public."ProductMultilingual" OWNER TO root;

--
-- Name: Sex; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public."Sex" (
    "Sex_ID" bigint NOT NULL,
    "SexCode" character varying(1)
);


ALTER TABLE public."Sex" OWNER TO root;

--
-- Name: SexMultilingual; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public."SexMultilingual" (
    "Sex_ID" bigint NOT NULL,
    "Language_ID" integer NOT NULL,
    "Name" character varying(255),
    "Description" character varying(1000)
);


ALTER TABLE public."SexMultilingual" OWNER TO root;

--
-- Name: State; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public."State" (
    "State_ID" integer NOT NULL,
    "StateCode" character varying(16),
    "Country_ID" integer
);


ALTER TABLE public."State" OWNER TO root;

--
-- Name: StateMultilingual; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public."StateMultilingual" (
    "State_ID" bigint NOT NULL,
    "Language_ID" integer NOT NULL,
    "Name" character varying(255),
    "Description" character varying(1000)
);


ALTER TABLE public."StateMultilingual" OWNER TO root;

--
-- Name: Unit; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public."Unit" (
    "Unit_ID" integer NOT NULL,
    "UnitCode" character varying(4)
);


ALTER TABLE public."Unit" OWNER TO root;

--
-- Name: UnitMultilingual; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public."UnitMultilingual" (
    "Unit_ID" integer NOT NULL,
    "Language_ID" integer NOT NULL,
    "Name" character varying(255),
    "Description" character varying(1000)
);


ALTER TABLE public."UnitMultilingual" OWNER TO root;

--
-- Name: User; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public."User" (
    "User_ID" numeric(22,0) NOT NULL,
    "UserLogin" character varying(255),
    "UserPassword" character varying(255),
    "Company_ID" bigint
);


ALTER TABLE public."User" OWNER TO root;

--
-- Name: Vat; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public."Vat" (
    "Vat_ID" integer NOT NULL,
    "VatCode" character varying(255),
    "State_ID" integer,
    "Country_ID" integer,
    "VatRate" numeric(12,4)
);


ALTER TABLE public."Vat" OWNER TO root;

--
-- Name: VatMultilingual; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public."VatMultilingual" (
    "Vat_ID" bigint NOT NULL,
    "Language_ID" integer NOT NULL,
    "Name" character varying(255),
    "Description" character varying(1000)
);


ALTER TABLE public."VatMultilingual" OWNER TO root;

--
-- Name: BankMultilingual BankMultilingual_pk; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public."BankMultilingual"
    ADD CONSTRAINT "BankMultilingual_pk" PRIMARY KEY ("Bank_ID", "Language_ID");


--
-- Name: Bank Bank_pk; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public."Bank"
    ADD CONSTRAINT "Bank_pk" PRIMARY KEY ("Bank_ID");


--
-- Name: CityMultilingual CityMultilingual_pk; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public."CityMultilingual"
    ADD CONSTRAINT "CityMultilingual_pk" PRIMARY KEY ("City_ID", "Language_ID");


--
-- Name: City City_pk; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public."City"
    ADD CONSTRAINT "City_pk" PRIMARY KEY ("City_ID");


--
-- Name: Company Company_pk; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public."Company"
    ADD CONSTRAINT "Company_pk" PRIMARY KEY ("Company_ID");


--
-- Name: CountryMultilingual CountryMultilingual_pk; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public."CountryMultilingual"
    ADD CONSTRAINT "CountryMultilingual_pk" PRIMARY KEY ("Country_ID", "Language_ID");


--
-- Name: Country Country_pk; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public."Country"
    ADD CONSTRAINT "Country_pk" PRIMARY KEY ("Country_ID");


--
-- Name: CurrencyExchange CurrencyExchange_pk; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public."CurrencyExchange"
    ADD CONSTRAINT "CurrencyExchange_pk" PRIMARY KEY ("Currency_ID");


--
-- Name: Currency Currency_pk; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public."Currency"
    ADD CONSTRAINT "Currency_pk" PRIMARY KEY ("Currency_ID");


--
-- Name: Customer Customer_pk; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public."Customer"
    ADD CONSTRAINT "Customer_pk" PRIMARY KEY ("Customer_ID");


--
-- Name: Date Date_pk; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public."Date"
    ADD CONSTRAINT "Date_pk" PRIMARY KEY ("Date_ID");


--
-- Name: InvoiceHeader InvoiceHeader_pk; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public."InvoiceHeader"
    ADD CONSTRAINT "InvoiceHeader_pk" PRIMARY KEY ("Invoice_ID");


--
-- Name: InvoicePosition InvoicePosition_pk; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public."InvoicePosition"
    ADD CONSTRAINT "InvoicePosition_pk" PRIMARY KEY ("Invoice_ID");


--
-- Name: Language Language_pk; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public."Language"
    ADD CONSTRAINT "Language_pk" PRIMARY KEY ("Language_ID");


--
-- Name: ProductGroupMultilingual ProductGroupMultilingual_pk; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public."ProductGroupMultilingual"
    ADD CONSTRAINT "ProductGroupMultilingual_pk" PRIMARY KEY ("ProductGroup_ID", "Language_ID");


--
-- Name: ProductGroupVat ProductGroupVat_pk; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public."ProductGroupVat"
    ADD CONSTRAINT "ProductGroupVat_pk" PRIMARY KEY ("Vat_ID", "ProductGroup_ID");


--
-- Name: ProductGroup ProductGroup_pk; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public."ProductGroup"
    ADD CONSTRAINT "ProductGroup_pk" PRIMARY KEY ("ProducrGroup_ID");


--
-- Name: ProductMultilingual ProductMultilingual_pk; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public."ProductMultilingual"
    ADD CONSTRAINT "ProductMultilingual_pk" PRIMARY KEY ("Product_ID", "Language_ID");


--
-- Name: Product Product_pk; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public."Product"
    ADD CONSTRAINT "Product_pk" PRIMARY KEY ("Product_ID");


--
-- Name: SexMultilingual SexMultilingual_pk; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public."SexMultilingual"
    ADD CONSTRAINT "SexMultilingual_pk" PRIMARY KEY ("Sex_ID", "Language_ID");


--
-- Name: Sex Sex_pk; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public."Sex"
    ADD CONSTRAINT "Sex_pk" PRIMARY KEY ("Sex_ID");


--
-- Name: StateMultilingual StateMultilingual_pk; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public."StateMultilingual"
    ADD CONSTRAINT "StateMultilingual_pk" PRIMARY KEY ("State_ID", "Language_ID");


--
-- Name: State State_pk; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public."State"
    ADD CONSTRAINT "State_pk" PRIMARY KEY ("State_ID");


--
-- Name: UnitMultilingual UnitMultilingual_pk; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public."UnitMultilingual"
    ADD CONSTRAINT "UnitMultilingual_pk" PRIMARY KEY ("Unit_ID", "Language_ID");


--
-- Name: Unit Unit_pk; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public."Unit"
    ADD CONSTRAINT "Unit_pk" PRIMARY KEY ("Unit_ID");


--
-- Name: User User_pk; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public."User"
    ADD CONSTRAINT "User_pk" PRIMARY KEY ("User_ID");


--
-- Name: VatMultilingual VatMultilingual_pk; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public."VatMultilingual"
    ADD CONSTRAINT "VatMultilingual_pk" PRIMARY KEY ("Vat_ID", "Language_ID");


--
-- Name: Vat Vat_pk; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public."Vat"
    ADD CONSTRAINT "Vat_pk" PRIMARY KEY ("Vat_ID");


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE USAGE ON SCHEMA public FROM PUBLIC;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--


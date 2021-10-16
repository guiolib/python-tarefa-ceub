CREATE SCHEMA IF NOT EXISTS "tarefa-ceub";

CREATE  TABLE "tarefa-ceub"."tipo-gravidade" ( 
	"codigo-gravidade"   integer  NOT NULL ,
	"nome-gravidade"     integer  NOT NULL ,
	CONSTRAINT "pk_tipo-gravidade_codigo-gravidade" PRIMARY KEY ( "codigo-gravidade" )
 );

CREATE  TABLE "tarefa-ceub"."tipo-infracao" ( 
	"codigo-tipo-infracao" integer  NOT NULL ,
	"nome-tipo-infracao" integer  NOT NULL ,
	CONSTRAINT "pk_tipo-infracao_codigo-infracao" PRIMARY KEY ( "codigo-tipo-infracao" )
 );

CREATE  TABLE "tarefa-ceub"."tipo-infrator" ( 
	"codigo-infrator"    integer  NOT NULL ,
	"nome-infrator"      integer  NOT NULL ,
	CONSTRAINT "pk_tipo-infrator_codigo-infrator" PRIMARY KEY ( "codigo-infrator" )
 );

CREATE  TABLE "tarefa-ceub"."tipo-veiculo" ( 
	"codigo-veiculo"     integer  NOT NULL ,
	"nome-veiculo"       integer  NOT NULL ,
	CONSTRAINT "pk_tipo-veiculo_codigo-veiculo" PRIMARY KEY ( "codigo-veiculo" )
 );

CREATE  TABLE "tarefa-ceub".infracao ( 
	"codigo-infracao"    integer  NOT NULL ,
	"codigo-tipo-infracao" integer  NOT NULL ,
	"codigo-tipo-veiculo" integer  NOT NULL ,
	"codigo-tipo-infrator" integer  NOT NULL ,
	"codigo-tipo-gravidade" integer  NOT NULL ,
	"horario-infracao"   timestamp   ,
	rodovia              text   ,
	"km-rodovia"         text   ,
	"local-complemento"  date   ,
	"local-longitude"    numeric   ,
	"local-latitude"     numeric   ,
	CONSTRAINT "pk_infracao_codigo-infracao" PRIMARY KEY ( "codigo-infracao" )
 );

ALTER TABLE "tarefa-ceub".infracao ADD CONSTRAINT "fk_infracao_tipo-infracao" FOREIGN KEY ( "codigo-tipo-infracao" ) REFERENCES "tarefa-ceub"."tipo-infracao"( "codigo-tipo-infracao" );

ALTER TABLE "tarefa-ceub".infracao ADD CONSTRAINT "fk_infracao_tipo-gravidade" FOREIGN KEY ( "codigo-tipo-gravidade" ) REFERENCES "tarefa-ceub"."tipo-gravidade"( "codigo-gravidade" );

ALTER TABLE "tarefa-ceub".infracao ADD CONSTRAINT "fk_infracao_tipo-infrator" FOREIGN KEY ( "codigo-tipo-infrator" ) REFERENCES "tarefa-ceub"."tipo-infrator"( "codigo-infrator" );

ALTER TABLE "tarefa-ceub".infracao ADD CONSTRAINT "fk_infracao_tipo-veiculo" FOREIGN KEY ( "codigo-tipo-veiculo" ) REFERENCES "tarefa-ceub"."tipo-veiculo"( "codigo-veiculo" );

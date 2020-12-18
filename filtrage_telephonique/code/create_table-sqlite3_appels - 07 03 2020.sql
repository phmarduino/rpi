begin;
create table phm_appels (nu_appel integer primary key autoincrement, date_modem date, heure_modem time, num_tel text, nom_appel text, ind_liste text, ind_rejet text, date_enreg date, heure_enreg time);
commit;

begin;
insert into phm_appels(date_modem, heure_modem, num_tel, nom_appel) values(date('now'), time('now'), "nutel1", "nom1");
insert into phm_appels(date_modem, heure_modem, num_tel, nom_appel) values(date('now'), time('now'), "nutel1", "nom2");
commit;

begin;
select * from phm_appels
commit;


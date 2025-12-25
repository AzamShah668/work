create table if not exists duas (
    id serial primary key,
    dua_text text not null
);

insert into duas (dua_text) values
('Allahumma inni as''aluka al-afiyah'),
('Rabbana la tuzigh quloobana ba’da idh hadaytana'),
('Allahumma barik lana fi rizqina'),
('HasbiAllahu la ilaha illa Huwa');


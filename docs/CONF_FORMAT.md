# Описание параметров конфигурации

- `api_id` - целочисленное значение, полученное с [my.telegram.org](https://my.telegram.org);
- `api_hash` - строковое значение, полученное с [my.telegram.org](https://my.telegram.org);
- `session_id` - идентификатор сессии (а также имя файла сессии) TGA из 8 случайных байт;
- `db_path` - путь до базы данных, по дефолту `db_path = 'storage/' + session_id + '.db'`

/* Drop tables */

drop table if exist dev1;
drop table if exist dev2;

/* Create dev1 and dev2 */
create table dev1 (id INT AUTO_INCREMENT, date DATETIME, ipaddr VARCHAR(15), process VARCHAR(256), command VARCHAR(256), command_parameters VARCHAR(1024), invoker_command VARCHAR(256), uid INTEGER(6), euid INTEGER(6), gid INTEGER(6), egid INTEGER(6), parent_command VARCHAR(256), puid INTEGER(6), peuid INTEGER(6), pgid INTEGER(6), pegid INTEGER(6), PRIMARY KEY(ID), CONSTRAINT Log UNIQUE (date, ipaddr, process, command, command_parameters, invoker_command, uid, euid, gid, egid, parent_command, puid, peuid, pgid, pegid) );

create table dev2 (id INT AUTO_INCREMENT, date DATETIME, ipaddr VARCHAR(15), process VARCHAR(256), command VARCHAR(256), command_parameters VARCHAR(1024), invoker_command VARCHAR(256), uid INTEGER(6), euid INTEGER(6), gid INTEGER(6), egid INTEGER(6), parent_command VARCHAR(256), puid INTEGER(6), peuid INTEGER(6), pgid INTEGER(6), pegid INTEGER(6), PRIMARY KEY(ID), CONSTRAINT Log UNIQUE (date, ipaddr, process, command, command_parameters, invoker_command, uid, euid, gid, egid, parent_command, puid, peuid, pgid, pegid) );

/* Create master_val which holds a master dictionary that will be used by our learning file */
create table master_val (command VARCHAR(60), frequency VARCHAR(6), class VARCHAR(30));

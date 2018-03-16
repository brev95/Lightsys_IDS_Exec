/* Drop and Create new database  */
drop database if exists grsecure_log;
create database grsecure_log;

use grsecure_log;

/* Drop tables */

drop table if exists dev1;
drop table if exists dev2;

/* Create dev1 and dev2 */
create table dev1 (id INT AUTO_INCREMENT, date DATETIME, ipaddr VARCHAR(15), process VARCHAR(256), command VARCHAR(256), command_parameters VARCHAR(1024), invoker_command VARCHAR(256), uid INTEGER(6), euid INTEGER(6), gid INTEGER(6), egid INTEGER(6), parent_command VARCHAR(256), puid INTEGER(6), peuid INTEGER(6), pgid INTEGER(6), pegid INTEGER(6), PRIMARY KEY(ID) table dev2 (id INT AUTO_INCREMENT, date DATETIME, ipaddr VARCHAR(15), process VARCHAR(256), command VARCHAR(256), command_parameters VARCHAR(1024), invoker_command VARCHAR(256), uid INTEGER(6), euid INTEGER(6), gid INTEGER(6), egid INTEGER(6), parent_command VARCHAR(256), puid INTEGER(6), peuid INTEGER(6), pgid INTEGER(6), pegid INTEGER(6), PRIMARY KEY(ID)  );

/* Create master_val which holds a master dictionary that will be used by our learning file */
create table master_val (command VARCHAR(256), frequency INTEGER(6), class VARCHAR(30));

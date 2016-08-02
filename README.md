# eubra_bigsea

Version Control

- This program deal with json tweets and retrieve the information about selected users.

Call of the last version:
python automatic_tweets_json_v1.py -i [1] -o [2] -c [3]

[1] json file of the tweets with the seletected fields {Required}
[2] name of the output file {Required}
[3] name of the city to be evaluate {Required}
[4] File .csv with the ID of each selected users {Not Required}
[5] begin date (It needs to be done) {Not Required}
[6] end date (It needs to be done) {Not Required}

- City to be evaluate:
 1. Belo horizonte - Use "bh" at -c parameter (without quotes "");
 2. Brasilia - "bsb";
 3. Curitiba - "ctba";
 4.  Fortaleza - "forz";
 5.  Manaus - "man";
 6.  Porto Alegre - "poal";
 7.  Recife - "rec";
 8. Rio de Janeiro - "rj"
 9. Sao Paulo - "sp";
 10. Salvador - "ssa"
 11. All - "all" to make the characterization of all cities

-----------------------------------------------------------------------------------------

- This program deal with json file to generate the statisticas about it

Call of the statistics.py:

python statistics.py -i [1] -p [2] 

[1] Json input file.

[2] File that owns information about selected users of twitter




------------------------------------------------------------------------------------------


- This program deal with two dates to perform a dump and select the immportant fields

Call of the script_datedump_selectfields.py:

python script_datedump_selectfields.py -s [1] -p [2] -d [3] -c [4] -sd [5] -ed [6] -o [7] test

[1] 'Name of the MongoDB server', required=True.

[2] 'Name of the MongoDB persistence slave', required=False.

[3] 'Name of the MongoDB database', required=True.

[4] 'Name of the MongoDB collection', required=True.

[5] 'The date when a project or task is scheduled to begin/start that define  the begin of the dump', required=True. Date on this format: "2016-03-30 00:00:00".Hour defined by UTC.

[6] 'The date when a project or task is scheduled to finish/end that define the end of the dump', required=True. Date on this format: "2016-03-30 00:00:00".Hour define
d by UTC.

[7] 'Name of the output file', required=True.


- Suggestions
@ Authors: 
	- Gustavo P. Avelar  (gpavelar)
	e-mail:gpavelardev@gmail.com
        - Rodrigo (rodrigo94)
	e-mail:
 


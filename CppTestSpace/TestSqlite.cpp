#include<sqlite3.h>
#include<iostream>


using namespace std;

// This is the callback function to display the select data in the table
static int callback1(void *NotUsed, int argc, char **argv, char **szColName)
{
  for(int i = 0; i < argc; i++)
  {
    std::cout << szColName[i] << " = " << argv[i] << std::endl;
  }

  std::cout << "\n";

  return 0;
}

int main()
{
	char *dblocation = "/home/phcostello/Documents/Data/FinanceData.sqlite";

	sqlite3 *db;

	cout << dblocation << endl;

	int rc = sqlite3_open(dblocation, &db);
	if(rc)
	{
		std::cout << "Can't open database\n";
	} else {
		std::cout << "Open database successfully\n";
	}



	char *sqlQry = "SELECT * FROM BA";

	char *szErrMsg;
	rc = sqlite3_exec(db, sqlQry,callback1,0, &szErrMsg );
	if(rc != SQLITE_OK)
	{
		cout << "SQL ERROR: " << szErrMsg << endl;
		sqlite3_free(szErrMsg);

	}

	if(db)
	{
		sqlite3_close(db);
	}


	return 0;
}

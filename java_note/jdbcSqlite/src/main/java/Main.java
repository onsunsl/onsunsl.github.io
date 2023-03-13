import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.Statement;

public class Main {
    public static void main(String[] args) throws Exception{
        Connection c = null;
        Statement stmt = null;

            c = DriverManager.getConnection("jdbc:sqlite:data.db");
            stmt = c.createStatement();
            System.out.println("删除表");
            stmt.execute("drop table if exists person");

            System.out.println("新建表");
            stmt.execute("create table if not exists `person`" +
                    "(`id` integer not null primary key AUTOINCREMENT," +
                    "`name` text," +
                    "`age` integer)");

            System.out.println("插入");
            stmt.execute("insert into person (name, age) values('张三', 23);");


        System.out.println("查询");
        stmt.execute("select * from person;");
        stmt.close();
        c.close();

    }
}

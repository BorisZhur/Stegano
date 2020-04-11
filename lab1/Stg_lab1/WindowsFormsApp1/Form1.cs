using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.IO;

namespace WindowsFormsApp1
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
            
        }
        public static string initStr = "абвгдежзийклмнопрстуфхцчшщъыьэюя.,!?";
        public static string rusLetters = "абвгдежзийклмнопрстуфхцчшщъыьэюя";
        public static string engLetters = "abcdefghijklmnopqrstuvwxyz";

        private void button1_Click(object sender, EventArgs e)
        {
            //StreamReader inp = new StreamReader("" + textBox1.Text + ".txt", Encoding.GetEncoding(1251));

        }
    }
}

using MySql.Data.MySqlClient;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using MySql.Data.MySqlClient;

namespace _3OLIDTS_JonathanCorzo_05
{
    public partial class Form1 : Form
    {
        private string conexionSQL = "Server=localhost;Port=3306;Database=programacionavanzada;Uid=root;Pwd=;";
        public Form1()
        {
            InitializeComponent();
            if (btnBuscar != null)
            {
                btnBuscar.Click += btnBuscar_Click;
            }
            CargarRegistrosEnGrid();
            ChecarDatagrid();
        }

        private DataTable ObtenerRegistros(string filtro = null)
        {
            string sql;
            if (string.IsNullOrEmpty(filtro))
            {
                sql = @"SELECT Id, Nombre, Apellidos, Edad, Estatura, Telefono, Genero FROM registros ORDER BY Id DESC;";
            }
            else
            {
                sql = @"SELECT Id, Nombre, Apellidos, Edad, Estatura, Telefono, Genero FROM registros WHERE Nombre LIKE @filtro OR Apellidos LIKE @filtro OR Telefono LIKE @filtro ORDER BY Id DESC;";
            }

            using (MySqlConnection connection = new MySqlConnection(conexionSQL))
            using (MySqlCommand cmd = new MySqlCommand(sql, connection))
            {
                if (!string.IsNullOrEmpty(filtro))
                {
                    cmd.Parameters.AddWithValue("@filtro", "%" + filtro + "%");
                }

                using (MySqlDataAdapter adapter = new MySqlDataAdapter(cmd))
                {
                    DataTable table = new DataTable();
                    adapter.Fill(table);
                    return table;
                }
            }
        }

        private void CargarRegistrosEnGrid()
        {
            try
            {
                DataTable dt = ObtenerRegistros();
                dgvConsulta.DataSource = null;
                dgvConsulta.DataSource = dt;

                if (dgvConsulta.Columns.Contains("Id"))
                {
                    dgvConsulta.Columns["Id"].Visible = true;
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Error al cargar datos: {ex.Message}", "Error BD", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void ChecarDatagrid()
        {
            if (dgvConsulta == null)
            {
                dgvConsulta = new DataGridView();
                dgvConsulta.Name = "dgvConsulta";
                dgvConsulta.Dock = DockStyle.Fill;
                dgvConsulta.ReadOnly = true;
                dgvConsulta.AllowUserToAddRows = false;
                dgvConsulta.AllowUserToDeleteRows = false;
                dgvConsulta.SelectionMode = DataGridViewSelectionMode.FullRowSelect;
                dgvConsulta.AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.Fill;
                this.Controls.Add(dgvConsulta);
            }
        }

        private void btnBuscar_Click(object sender, EventArgs e)
        {
            string filtro = tbParametro.Text.Trim();
            try
            {
                DataTable resultados = ObtenerRegistros(filtro);
                dgvConsulta.DataSource = null;
                dgvConsulta.DataSource = resultados;

                if (resultados.Rows.Count == 0)
                {
                    MessageBox.Show("No se encontraron registros con ese criterio.", "Sin resultados", MessageBoxButtons.OK, MessageBoxIcon.Information);
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show("Error en la búsqueda: " + ex.Message, "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }
    }
}
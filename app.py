from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, NumberRange
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '2417'

class CotizacionForm(FlaskForm):
    numeroCotizacion = StringField('N° Cotización', validators=[DataRequired()])

@app.route('/')
def index():
    # Esta es la vista principal que muestra el formulario
    return render_template('index.html')

@app.route('/guardar_cotizacion', methods=['POST'])
def guardar_cotizacion():
        numero_cotizacion = request.form.get('numeroCotizacion')

        # Imprimir el número de cotización para propósitos de depuración
        print("Número de Cotización recibido:", numero_cotizacion)

        # Validar el número de cotización (este es un ejemplo simple de validación)
        if not numero_cotizacion:
            # Manejar el error, por ejemplo, reenviando al usuario al formulario con un mensaje de error
            error = "El número de cotización es requerido."
            return render_template('index.html', error=error)

        # Guardar en archivo CSV
        #with open('cotizaciones.csv', mode='a', newline='') as file:
        #    writer = csv.writer(file)
        #    writer.writerow([numero_cotizacion])
        
        # Redirigir a la misma página para evitar el reenvío del formulario
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
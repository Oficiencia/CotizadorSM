from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, SubmitField, BooleanField
from wtforms.validators import DataRequired, NumberRange, Optional, InputRequired
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '2417'

class CotizacionForm(FlaskForm):
    numeroCotizacion = StringField('N° Cotización', validators=[DataRequired()])
    codigoProducto = StringField('Código del Producto', validators=[Optional()])
    familiaProducto = StringField('Familia del Producto', validators=[DataRequired()])
    nombreProducto = StringField('Nombre del Producto', validators=[DataRequired()])
    cliente = StringField('Cliente', validators=[DataRequired()])
    peso = FloatField('Peso (gr)', validators=[DataRequired(), NumberRange(min=0.01)])
    porcentajeAumento = FloatField('% Aumento', validators=[InputRequired()], default=10.0)
    material1 = StringField('Material 1', validators=[DataRequired()])
    costoMaterial1 = FloatField('Costo Material 1', validators=[DataRequired()])
    porcentajeMat1 = FloatField('% Mat1', validators=[DataRequired(), NumberRange(min=0, max=100)])
    material2 = StringField('Material 2', validators=[Optional()])
    costoMaterial2 = FloatField('Costo Material 2', validators=[Optional()])
    porcentajeMat2 = FloatField('% Mat2', validators=[Optional(), NumberRange(min=0, max=100)])
    pigmento = StringField('Pigmento', validators=[DataRequired()])
    costoPigmento = FloatField('Costo Pigmento', validators=[InputRequired()])
    undsPorEmpaque = IntegerField('# unds por empaque', validators=[DataRequired()])
    incluyeCaja = BooleanField('Caja')  
    tamanoCaja = StringField('Tamaño', validators=[Optional()])
    costoCaja = FloatField('Costo', validators=[Optional()])
    incluyeBolsa = BooleanField('Bolsa') 
    costoRollo = FloatField('Costo Rollo', validators=[Optional()])
    bolsasPorRollo = FloatField('Bolsas por rollo', validators=[Optional()])
    cavidades = IntegerField('# Cavidades', validators=[DataRequired()])
    ciclo = FloatField('Ciclo (Segundos)', validators=[DataRequired()])
    maquinaCotizacion = StringField('Máquina', validators=[DataRequired()])
    productoFrecuenteCotizacion = StringField('Producto que más se fabrica', validators=[DataRequired()])
    porcentajeMPPrecio = FloatField('% MP / Precio', validators=[DataRequired()])
    truputSeg = FloatField('Truput x seg', validators=[DataRequired()])
    ensambleProductos = BooleanField('Ensamble con otros productos')
    numeroDePartes = IntegerField('Número de partes', validators=[Optional()], default=0)
    linners = BooleanField('Linners')
    refLinner = StringField('Referencia', validators=[Optional()])
    precioPorUndLinner = FloatField('Costo por Und', validators=[Optional()])
    maquinaPorUndLinner = FloatField('Maquina por Und', validators=[Optional()])
    personasLinner = IntegerField('# Personas', validators=[Optional()])
    piezasPorTurnoLinner = IntegerField('Piezas por turno', validators=[Optional()])
    etiquetas = BooleanField('Etiquetas')
    refetiqueta = StringField('Referencia', validators=[Optional()])
    precioPorUndEtiqueta = FloatField('Costo por Und', validators=[Optional()])
    maquinaPorUndEtiqueta = FloatField('Maquina por Und', validators=[Optional()])
    personasEtiqueta = IntegerField('# Personas', validators=[Optional()])
    piezasPorTurnoEtiqueta = IntegerField('Piezas por turno', validators=[Optional()])
    guardar = SubmitField('Guardar Cotización')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = CotizacionForm()
    if form.validate_on_submit():
        numero_cotizacion = form.numeroCotizacion.data
        codigo_producto = form.codigoProducto.data
        familia_producto = form.familiaProducto.data
        nombre_producto = form.nombreProducto.data
        cliente = form.cliente.data
        peso = form.peso.data
        porcentaje_aumento = form.porcentajeAumento.data
        material1 = form.material1.data
        costo_material1 = form.costoMaterial1.data
        porcentaje_mat1 = form.porcentajeMat1.data
        material2 = form.material2.data if porcentaje_mat1 < 100 else ''
        costo_material2 = form.costoMaterial2.data if porcentaje_mat1 < 100 else ''
        porcentaje_mat2 = form.porcentajeMat2.data if porcentaje_mat1 < 100 else ''
        pigmento = form.pigmento.data
        costo_pigmento = form.costoPigmento.data
        undsPorEmpaque = form.undsPorEmpaque.data
        cavidades = form.cavidades.data
        ciclo = form.ciclo.data
        maquinaCotizacion = form.maquinaCotizacion.data
        productoFrecuenteCotizacion = form.productoFrecuenteCotizacion.data
        porcentajeMPPrecio = form.porcentajeMPPrecio.data
        truputSeg = form.truputSeg.data
        ensambleProductos = form.ensambleProductos.data
        numeroDePartes = int(form.numeroDePartes.data) if ensambleProductos else 0

        costoMat_por_und = request.form.get('costoMatPorUnd')
        costoPig_por_und = request.form.get('costoPigPorUnd')
        costoCaja_por_und = request.form.get('costoCajaPorUnd')
        costoBolsa_por_und = request.form.get('costoBolsaporUnd')
        costo_MP = request.form.get('costoMP')
        cantidadMin = request.form.get('cantidadMin')
        cantidadMinColor = request.form.get('cantidadMinColor')
        cantidadMax = request.form.get('cantidadMax')
        precioMetodo1 = request.form.get('precioMetodo1')
        truputSegMetodo1 = request.form.get('truputSegMetodo1')
        precioMetodo2 = request.form.get('precioMetodo2')
        porcentajeMPPrecioMetodo2 = request.form.get('porcentajeMPPrecioMetodo2')
        precioMin = request.form.get('precioMin')
        costoEnsambleProductos = request.form.get('costoEnsambleProductos')
        costoEnsambleLinner = request.form.get('costoEnsambleLinner')
        costoLinners = request.form.get('costoLinners')
        costoPosturaEtiqueta = request.form.get('costoPosturaEtiqueta')
        costoEtiquetas = request.form.get('costoEtiquetas')

        # Imprimir campos
        print("Número de Cotización recibido:", numero_cotizacion)
        print("Código del Producto recibido:", codigo_producto)
        print("Familia del Producto recibido:", familia_producto)
        print("Nombre del Producto recibido:", nombre_producto)
        print("Cliente recibido:", cliente)
        print("Peso recibido:", peso)
        print("% Aumento recibido:", porcentaje_aumento)
        print("Material 1:", material1, "Costo Material 1:", costo_material1)
        print("% Mat1:", porcentaje_mat1)
        print("Material 2:", material2)
        print("Costo Material 2:", costo_material2)
        print("% Mat2:", porcentaje_mat2)
        print("Costo MP por und recibido:", costoMat_por_und)
        print("Pigmento recibido:", pigmento)
        print("Costo Pigmento recibido:", costo_pigmento)
        print("Costo Pig por und recibido:", costoPig_por_und)
        print("Unds por empaque recibido:", undsPorEmpaque)

        if form.incluyeCaja.data:  # Si el checkbox está marcado
            tamano_caja = form.tamanoCaja.data
            costo_caja = form.costoCaja.data
        else:
            # Si 'incluyeCaja' no está marcado, establece 'tamano_caja' y 'costo_caja' como vacíos
            tamano_caja = ''
            costo_caja = ''

        print("Tamaño de la caja:", tamano_caja)
        print("Costo de la caja:", costo_caja)
        print("Costo Caja por und recibido:", costoCaja_por_und)

        if form.incluyeBolsa.data:  # Si el checkbox está marcado
            costo_rollo = form.costoRollo.data
            bolsasPorRollo = form.bolsasPorRollo.data
        else:
            # Si 'incluyeBolsa' no está marcado, establece 'costo_rollo' y 'bolsasPorRollo' como vacíos
            costo_rollo = ''
            bolsasPorRollo = ''

        print("Costo del rollo:", costo_rollo)
        print("Bolsas por rollo:", bolsasPorRollo)
        print("Costo bolsa por und recibido:", costoBolsa_por_und)
        print("Costo MP por und recibido:", costo_MP)
        print("# Cavidades recibido:", cavidades)
        print("Ciclo recibido:", ciclo)
        print("Cantidad Mínima recibida:", cantidadMin)
        print("Cant Mín Color recibida:", cantidadMinColor)
        print("Cantidad Máx recibida:", cantidadMax)
        print("Máquina recibida:", maquinaCotizacion)
        print("Producto frecuente recibido:", productoFrecuenteCotizacion)
        print("% MP / Precio recibido:", porcentajeMPPrecio)
        print("Truput x seg recibido:", truputSeg)
        print("Precio Método 1 recibido:", precioMetodo1)
        print("Truput x seg Método 1 recibido:", truputSegMetodo1)
        print("Precio Método 2 recibido:", precioMetodo2)
        print("% MP / Precio Método 2 recibido:", porcentajeMPPrecioMetodo2)
        print("Precio Mín recibido:", precioMin)

        print(f"Ensamble con otros productos: {ensambleProductos}, Número de partes: {numeroDePartes}")
        
        partes = []
        for i in range(1, numeroDePartes + 1):
            parte = {
                'numeroParte': request.form.get(f'numeroParte{i}', ''),
                'precioPorUnd': request.form.get(f'precioPorUnd{i}', ''),
                'maquinaEnsamble': request.form.get(f'maquinaEnsamble{i}', ''),
                'numeroPersonas': request.form.get(f'numeroPersonas{i}', ''),
                'piezasXTurno': request.form.get(f'piezasXTurno{i}', ''),
                'costoEnsamble': request.form.get(f'costoEnsamble{i}', ''),
                'total': request.form.get(f'total{i}', '')
            }
            partes.append(parte)
            print(f"Parte {i}: {parte}")
        
        print("Costo Total Ensamble recibido:", costoEnsambleProductos)

        if form.linners.data:
            refLinner = form.refLinner.data
            precioPorUndLinner = form.precioPorUndLinner.data
            maquinaPorUndLinner = form.maquinaPorUndLinner.data
            personasLinner = form.personasLinner.data
            piezasPorTurnoLinner = form.piezasPorTurnoLinner.data
            print(f"Ref. Linner: {refLinner}")
            print(f"Costo por Und Linner: {precioPorUndLinner}")
            print(f"Maq por und. Linner: {maquinaPorUndLinner}")
            print(f"Personas. Linner: {personasLinner}")
            print(f"Piezas por Turno. Linner: {piezasPorTurnoLinner}")
            print(f"Costo Ensamble Linner: {costoEnsambleLinner}")
            print(f"Costo Linner: {costoLinners}")
        
        if form.etiquetas.data:
            refetiqueta = form.refetiqueta.data
            precioPorUndEtiqueta = form.precioPorUndEtiqueta.data
            maquinaPorUndEtiqueta = form.maquinaPorUndEtiqueta.data
            personasEtiqueta = form.personasEtiqueta.data
            piezasPorTurnoEtiqueta = form.piezasPorTurnoEtiqueta.data
            print(f"Ref. Etiqueta: {refetiqueta}")
            print(f"Costo por Und Etiqueta: {precioPorUndEtiqueta}")
            print(f"Maq por und. Etiqueta: {maquinaPorUndEtiqueta}")
            print(f"Personas. Etiqueta: {personasEtiqueta}")
            print(f"Piezas por Turno. Etiqueta: {piezasPorTurnoEtiqueta}")
            print(f"Costo Ensamble Etiqueta: {costoPosturaEtiqueta}")
            print(f"Costo Etiqueta: {costoEtiquetas}")

        # Guardar en archivo CSV
        #with open('cotizaciones.csv', mode='a', newline='') as file:
        #    writer = csv.writer(file)
        #    writer.writerow([numero_cotizacion])

        flash('Cotización guardada con éxito!', 'success')
        # Redirigir a la misma página para evitar el reenvío del formulario
        return redirect(url_for('index'))
        
    # Esta es la vista principal que muestra el formulario
    return render_template('index.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
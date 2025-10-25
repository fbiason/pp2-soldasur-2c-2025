"""
test_product_loader.py - Script de prueba del cargador de productos

Este script verifica que el sistema experto carga correctamente los productos
desde el archivo Excel Products_db.xlsx.
"""

import sys
from pathlib import Path

# Agregar el directorio raíz al path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from app.modules.expertSystem.product_loader import get_product_loader


def test_product_loading():
    """Prueba la carga de productos desde Excel"""
    print("=" * 60)
    print("TEST: CARGA DE PRODUCTOS DESDE EXCEL")
    print("=" * 60)
    
    loader = get_product_loader()
    
    # Verificar radiadores
    radiators = loader.get_radiators_dict()
    print(f"\n✓ Radiadores cargados: {len(radiators)}")
    if radiators:
        print("\nPrimeros 3 radiadores:")
        for i, (name, model) in enumerate(list(radiators.items())[:3], 1):
            print(f"  {i}. {name}")
            print(f"     - Potencia: {model['potencia']:.2f} kcal/h")
            print(f"     - Coeficiente: {model['coeficiente']}")
            print(f"     - Colores: {', '.join(model['colors'])}")
    
    # Verificar calderas
    boilers = loader.get_boilers_list()
    print(f"\n✓ Calderas cargadas: {len(boilers)}")
    if boilers:
        print("\nPrimeras 3 calderas:")
        for i, boiler in enumerate(boilers[:3], 1):
            print(f"  {i}. {boiler['name']}")
            print(f"     - Potencia: {boiler['potencia_kcal']:.2f} kcal/h")
            print(f"     - Tipo: {boiler['type']}")
    
    # Verificar piso radiante
    floor = loader.get_floor_heating_list()
    print(f"\n✓ Sistemas de piso radiante: {len(floor)}")
    
    # Total de productos
    all_products = loader.get_all_products()
    print(f"\n✓ TOTAL DE PRODUCTOS: {len(all_products)}")
    
    return len(all_products) > 0


def test_radiator_filtering():
    """Prueba el filtrado de radiadores"""
    print("\n" + "=" * 60)
    print("TEST: FILTRADO DE RADIADORES")
    print("=" * 60)
    
    loader = get_product_loader()
    
    # Caso de prueba: Buscar radiadores modernos blancos para 2000 kcal/h
    print("\nBuscando radiadores:")
    print("  - Instalación: cualquiera")
    print("  - Estilo: moderno")
    print("  - Color: blanco")
    print("  - Carga térmica: 2000 kcal/h")
    
    results = loader.filter_radiators_by_criteria(
        radiator_type='principal',
        installation='cualquiera',
        style='moderno',
        color='blanco',
        heat_load=2000
    )
    
    print(f"\n✓ Radiadores encontrados: {len(results)}")
    for i, rad in enumerate(results[:3], 1):
        potencia_efectiva = rad['potencia'] * rad['coeficiente']
        print(f"\n  {i}. {rad['name']}")
        print(f"     - Potencia efectiva: {potencia_efectiva:.2f} kcal/h")
        print(f"     - Diferencia: {abs(potencia_efectiva - 2000):.2f} kcal/h")
    
    return len(results) > 0


def test_boiler_recommendation():
    """Prueba la recomendación de calderas"""
    print("\n" + "=" * 60)
    print("TEST: RECOMENDACIÓN DE CALDERAS")
    print("=" * 60)
    
    loader = get_product_loader()
    
    # Buscar caldera para 25000 kcal/h
    power_required = 25000
    print(f"\nBuscando caldera para {power_required} kcal/h...")
    
    boiler = loader.find_boiler_by_power(power_required)
    
    if boiler:
        print(f"\n✓ Caldera recomendada: {boiler['name']}")
        print(f"  - Potencia: {boiler['potencia_kcal']:.2f} kcal/h")
        print(f"  - Tipo: {boiler['type']}")
        print(f"  - Descripción: {boiler['description'][:100]}...")
        return True
    else:
        print("✗ No se encontró caldera adecuada")
        return False


def test_export_catalog():
    """Prueba la exportación del catálogo a JSON"""
    print("\n" + "=" * 60)
    print("TEST: EXPORTACIÓN DE CATÁLOGO")
    print("=" * 60)
    
    loader = get_product_loader()
    
    output_path = "data/processed/products_catalog_test.json"
    print(f"\nExportando catálogo a {output_path}...")
    
    try:
        loader.export_to_json(output_path)
        
        # Verificar que el archivo existe
        if Path(output_path).exists():
            file_size = Path(output_path).stat().st_size
            print(f"✓ Archivo creado: {file_size} bytes")
            return True
        else:
            print("✗ El archivo no se creó")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def main():
    """Ejecuta todos los tests"""
    print("\n" + "=" * 60)
    print("SISTEMA EXPERTO - TEST DE BASE DE CONOCIMIENTO DINÁMICA")
    print("=" * 60)
    print("\nVerificando que el sistema experto carga productos desde Excel...")
    
    tests = [
        ("Carga de productos", test_product_loading),
        ("Filtrado de radiadores", test_radiator_filtering),
        ("Recomendación de calderas", test_boiler_recommendation),
        ("Exportación de catálogo", test_export_catalog)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n✗ Error en {test_name}: {e}")
            results.append((test_name, False))
    
    # Resumen
    print("\n" + "=" * 60)
    print("RESUMEN DE TESTS")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\nResultado: {passed}/{total} tests pasados")
    
    if passed == total:
        print("\n🎉 ¡Todos los tests pasaron! El sistema experto está usando")
        print("   correctamente la base de conocimiento desde Excel.")
    else:
        print("\n⚠️  Algunos tests fallaron. Revisa los errores arriba.")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

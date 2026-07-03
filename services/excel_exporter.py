from openpyxl import Workbook
from pathlib import Path
from datetime import datetime


class ExcelExporter:

    def export(self, houses):

        Path("exports").mkdir(exist_ok=True)

        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "Viviendas"

        sheet.append([
            "Portal",
            "Título",
            "Precio (€)",
            "Superficie (m²)",
            "Habitaciones",
            "Baños",
            "URL",
            "Primera detección"
        ])

        for house in houses:

            sheet.append([
                house.portal,
                house.title,
                house.price,
                house.size,
                house.bedrooms,
                house.bathrooms,
                house.url,
                house.first_seen
            ])

        

        filename = datetime.now().strftime(
            "exports/viviendas_%Y%m%d_%H%M%S.xlsx"
        )
        workbook.save(filename)

        print(f"📄 Excel exportado: {filename}")
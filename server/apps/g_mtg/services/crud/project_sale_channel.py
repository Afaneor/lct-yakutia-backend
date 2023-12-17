from typing import Any, Dict

from server.apps.g_mtg.models import Project, ProjectSaleChannel, SaleChannel


def get_correct_prompt(
    project: Project,
    sale_channel: SaleChannel,
) -> str:
    """Генерация корректной подсказки."""
    if project.description:
        return (
            'При формировании маркетингового предложения необходимо ' +
            'учитывать следующую информацию о поводе продажи, банковском ' +
            'продукте, который продается, канале продажи и клиенте. ' +
            'Повод продажи имеет следующие характеристики: ' +
            f'"{project.description}" ' +
            'Банковский продукт, который необходимо продать имеет следующие ' +
            'характеристики: ' +
            f'"{project.product.description}" ' +
            'Канал продажи, который будет использоваться для продвижения ' +
            'банковского продукта имеет следующие характеристики: ' +
            f'"{sale_channel.description}"'
        )
    return (
        'При формировании маркетингового предложения необходимо учитывать ' +
        'следующую информацию о продукте и канале продажи и клиенте. ' +
        'Банковский продукт, который необходимо продать имеет следующие ' +
        'характеристики. ' +
        f'"{project.product.description}" ' +
        'Канал продажи, который будет использоваться для продвижения ' +
        'банковского продукта имеет следующие характеристики. ' +
        f'"{sale_channel.description}"'
    )


def create_project_sale_channel(
    validated_data: Dict[str, Any],
) -> None:
    """Создание в проекте каналов связи."""
    project = validated_data['project']

    ProjectSaleChannel.objects.bulk_create(
        [
            ProjectSaleChannel(
                project=project,
                sale_channel=sale_channel,
                prompt=get_correct_prompt(
                    project=project,
                    sale_channel=sale_channel,
                )
            )
            for sale_channel in validated_data['sales_channels']
        ]
    )

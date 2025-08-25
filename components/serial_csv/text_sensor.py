import esphome.codegen as cg
import esphome.config_validation as cv
from esphome import automation
from esphome.components import uart
from esphome.components import text_sensor
from esphome.const import CONF_ID, CONF_INDEX, CONF_TEXT_SENSORS

CODEOWNERS = ["@ssieb"]

DEPENDENCIES = ['uart']

serial_ns = cg.esphome_ns.namespace('serial')

SerialCSV = serial_ns.class_('SerialCSV', cg.Component, text_sensor.TextSensor, uart.UARTDevice)

CONFIG_SCHEMA = uart.UART_DEVICE_SCHEMA.extend(
    {
        cv.GenerateID(): cv.declare_id(SerialCSV),
        cv.Required(CONF_TEXT_SENSORS): cv.ensure_list(
            text_sensor.text_sensor_schema().extend(
                {
                    cv.Required(CONF_INDEX): cv.positive_int,
                }
            )
        ),
    }
)

async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await uart.register_uart_device(var, config)
    for conf in config[CONF_TEXT_SENSORS]:
        sens = await text_sensor.new_text_sensor(conf)
        index = conf[CONF_INDEX]
        cg.add(var.add_text_sensor(index, sens))

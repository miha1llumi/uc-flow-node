import ujson
from typing import List, Tuple

from uc_flow_nodes.schemas import NodeRunContext
from uc_flow_nodes.service import NodeService
from uc_flow_nodes.views import info, execute
from uc_flow_schemas import flow
from uc_flow_schemas.flow import Property, CredentialProtocol, RunState
from uc_http_requester.requester import Request


class NodeType(flow.NodeType):
    id: str = '4a8ee635-f06e-4444-b51b-200b8d94798d'
    type: flow.NodeType.Type = flow.NodeType.Type.action
    name: str = 'Mihail'
    displayName: str = 's'
    icon: str = '<svg><text x="8" y="50" font-size="50">🤖</text></svg>'
    description: str = 'of course'
    properties: List[Property] = [
        Property(
            displayName='first_number',
            name='str_number',
            type=Property.Type.STRING,
            placeholder='Foo placeholder',
            description='Foo description',
            required=True,
            default='Test data',
        ),
        Property(
            displayName='second_number',
            name='number',
            type=Property.Type.NUMBER,
            placeholder='Foo placeholder',
            description='Foo description',
            required=True,
            default='Test data',
        ),
        Property(
            displayName='return int/str',
            name='multi_choice',
            type=Property.Type.BOOLEAN,
            placeholder='Foo placeholder',
            description='Foo description',
            required=True,
            default=False,
        ),
    ]


class InfoView(info.Info):
    class Response(info.Info.Response):
        node_type: NodeType


class ExecuteView(execute.Execute):
    async def post(self, json: NodeRunContext) -> NodeRunContext:
        figure_1 = int(json.node.data.properties['str_number'])
        figure_2 = json.node.data.properties['number']
        what_returns = str if json.node.data.properties['multi_choice'] else int

        result = figure_1 + figure_2 if what_returns is int else str(figure_1 + figure_2)
        try:
            await json.save_result({
                "result": result
            })
            json.state = RunState.complete
        except Exception as e:
            self.log.warning(f'Error {e}')
            await json.save_error(str(e))
            json.state = RunState.error
        return json


class Service(NodeService):
    class Routes(NodeService.Routes):
        Info = InfoView
        Execute = ExecuteView

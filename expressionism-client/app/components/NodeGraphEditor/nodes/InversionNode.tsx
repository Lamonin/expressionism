import { NodeProps } from "@xyflow/react";
import { BaseNode, InputHandle, OutputHandle } from "./NodePrimitives";
import { ExpressionismNode, OPERATION_NODES } from "./types";

const InversionNode: ExpressionismNode<NodeProps> = (props: NodeProps) => {
    return (
        <BaseNode title={InversionNode.label} color="violet" {...props}>
            <OutputHandle handleId="out-1" label="Результат"></OutputHandle>
            <InputHandle handleId="expression" label="Выражение"></InputHandle>
        </BaseNode>
    );
};

InversionNode.label = "Инверсия";
InversionNode.group = OPERATION_NODES;

export default InversionNode;

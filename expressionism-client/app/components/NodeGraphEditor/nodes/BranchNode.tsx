import { Button } from "primereact/button";
import { useEffect, useState } from "react";
import { NodeProps, useReactFlow, useUpdateNodeInternals } from "reactflow";
import { BaseNode, InputHandle, OutputHandle } from "./NodePrimitives";
import { InputField } from "./fields";

const BranchNode = (props: NodeProps) => {
    const { getNodes, setNodes } = useReactFlow();
    const updateNodeInternals = useUpdateNodeInternals();
    const [branches, setBranches] = useState(["", ""]);

    const setBranchesWrapper = (newBranches: string[]) => {
        setBranches(newBranches);
        setNodes(
            getNodes().map((node) => {
                if (node.id === props.id) {
                    node.data = {
                        ...node.data,
                        branches: newBranches,
                    };
                }
                return node;
            }),
        );
    };

    useEffect(() => {
        updateNodeInternals(props.id);
    }, [props.id, updateNodeInternals, branches]);

    return (
        <BaseNode title="Ветвление" color="lime" {...props}>
            <OutputHandle handleId="out-1" label="Результат"></OutputHandle>
            <OutputHandle handleId="selected-index" label="Индекс выбранного"></OutputHandle>
            {branches.map((branch, i) => (
                <InputHandle key={i} handleId={`branch-${i}`} label={`Выражение ${i + 1}`}>
                    <InputField
                        id={"1"}
                        value={branch}
                        placeholder="Введите выражение"
                        onChange={(e) => {
                            const newBranches = [...branches];
                            newBranches[i] = e.target.value;
                            setBranchesWrapper(newBranches);
                        }}
                    />
                    <Button
                        icon="pi pi-times"
                        size="small"
                        text
                        severity="danger"
                        style={{ padding: "2px", width: "28px" }}
                        disabled={i < 2}
                        onClick={() => {
                            setBranchesWrapper(branches.filter((_, j) => j !== i));
                        }}
                    />
                </InputHandle>
            ))}

            <Button
                icon="pi pi-plus"
                label="Новая ветвь"
                text
                size="small"
                style={{ padding: "2px 8px" }}
                disabled={branches.length >= 10}
                onClick={(e) => {
                    setBranchesWrapper(branches.concat(""));
                }}
            />
        </BaseNode>
    );
};

export default BranchNode;
